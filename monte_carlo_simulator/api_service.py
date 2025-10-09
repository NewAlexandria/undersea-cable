"""
FastAPI Web Service for DAS Monte Carlo Simulator
Provides REST API for running simulations and analyzing results
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import numpy as np

from das_monte_carlo import (
    DASMonteCarloSimulator,
    SimulationInputs,
    StochasticParameters,
    ArchitectureOption,
    SimulationOutputs,
    analyze_results
)

app = FastAPI(title="DAS Monte Carlo Simulator API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    """API request model for simulation"""
    # Strategic decisions
    architecture_option: str = "C"  # A, B, or C
    series_a_funding: float = 10_000_000
    compression_error_threshold: float = 0.1
    
    # Growth strategy
    initial_cables: int = 3
    target_cables_month_6: int = 5
    target_cables_month_12: int = 15
    target_cables_month_18: int = 30
    
    # Pricing
    pricing_port: float = 35_000
    pricing_naval: float = 500_000
    pricing_environmental: float = 10_000
    pricing_shipping: float = 10_000
    pricing_insurance: float = 25_000
    
    # Team
    initial_team_size: int = 5
    team_growth_rate: float = 1.5
    
    # Cloud
    cloud_provider: str = "GCP"
    cloud_credits_secured: float = 250_000
    
    # Simulation parameters
    simulation_months: int = 24
    num_simulations: int = 1000
    
    # Stochastic parameters (optional overrides)
    detection_accuracy_mean: Optional[float] = 0.97
    detection_accuracy_std: Optional[float] = 0.02
    conversion_rate_port_mean: Optional[float] = 0.25
    churn_rate_monthly_mean: Optional[float] = 0.02


class SimulationResponse(BaseModel):
    """API response model"""
    status: str
    analysis: Dict
    sample_trajectories: List[Dict]  # A few example trajectories


def convert_outputs_to_dict(outputs: SimulationOutputs) -> Dict:
    """Convert SimulationOutputs to JSON-serializable dict"""
    return {
        'months': outputs.months,
        'cables_deployed': outputs.cables_deployed,
        'total_customers': outputs.total_customers,
        'detection_accuracy': outputs.detection_accuracy,
        'detections_per_day': outputs.detections_per_day,
        'system_uptime': outputs.system_uptime,
        'regional_datacenters': outputs.regional_datacenters,
        'team_size_total': outputs.team_size_total,
        'revenue_monthly': outputs.revenue_monthly,
        'costs_monthly': outputs.costs_monthly,
        'gross_margin': outputs.gross_margin,
        'cash_remaining': outputs.cash_remaining,
        'arr': outputs.arr,
        'profitability_achieved': outputs.profitability_achieved,
        'profitability_month': outputs.profitability_month,
        'series_b_qualified': outputs.series_b_qualified,
        'ran_out_of_cash': outputs.ran_out_of_cash,
        'failure_month': outputs.failure_month
    }


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML interface"""
    with open("static/index.html", "r") as f:
        return f.read()


@app.post("/api/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """Run Monte Carlo simulation with provided parameters"""
    try:
        # Convert request to simulation inputs
        arch_map = {
            "A": ArchitectureOption.OPTION_A_GPU_EDGE,
            "B": ArchitectureOption.OPTION_B_REGIONAL_DC,
            "C": ArchitectureOption.OPTION_C_CLOUD_ONLY
        }
        
        inputs = SimulationInputs(
            architecture_option=arch_map.get(request.architecture_option, 
                                            ArchitectureOption.OPTION_C_CLOUD_ONLY),
            series_a_funding=request.series_a_funding,
            compression_error_threshold=request.compression_error_threshold,
            initial_cables=request.initial_cables,
            target_cables_month_6=request.target_cables_month_6,
            target_cables_month_12=request.target_cables_month_12,
            target_cables_month_18=request.target_cables_month_18,
            pricing_port=request.pricing_port,
            pricing_naval=request.pricing_naval,
            pricing_environmental=request.pricing_environmental,
            pricing_shipping=request.pricing_shipping,
            pricing_insurance=request.pricing_insurance,
            initial_team_size=request.initial_team_size,
            team_growth_rate=request.team_growth_rate,
            cloud_provider=request.cloud_provider,
            cloud_credits_secured=request.cloud_credits_secured,
            simulation_months=request.simulation_months
        )
        
        params = StochasticParameters(
            detection_accuracy_mean=request.detection_accuracy_mean,
            detection_accuracy_std=request.detection_accuracy_std,
            conversion_rate_port_mean=request.conversion_rate_port_mean,
            churn_rate_monthly_mean=request.churn_rate_monthly_mean
        )
        
        # Run simulation
        simulator = DASMonteCarloSimulator(inputs, params)
        results = simulator.run_monte_carlo(num_simulations=request.num_simulations)
        
        # Analyze results
        analysis = analyze_results(results)
        
        # Get sample trajectories (p10, median, p90)
        # Sort by final ARR
        sorted_results = sorted(results, key=lambda r: r.arr[-1] if r.arr else 0)
        
        sample_indices = [
            int(len(sorted_results) * 0.1),   # p10
            int(len(sorted_results) * 0.5),   # median
            int(len(sorted_results) * 0.9)    # p90
        ]
        
        sample_trajectories = []
        for idx in sample_indices:
            if idx < len(sorted_results):
                sample_trajectories.append(convert_outputs_to_dict(sorted_results[idx]))
        
        return SimulationResponse(
            status="success",
            analysis=analysis,
            sample_trajectories=sample_trajectories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/presets")
async def get_presets():
    """Get preset scenarios for quick testing"""
    presets = {
        "conservative": {
            "name": "Conservative Growth",
            "description": "Cloud-only, slower growth, lower risk",
            "architecture_option": "C",
            "target_cables_month_12": 10,
            "target_cables_month_18": 20,
            "pricing_port": 25_000,
            "series_a_funding": 10_000_000
        },
        "aggressive": {
            "name": "Aggressive Growth",
            "description": "Regional datacenter, faster growth, higher risk",
            "architecture_option": "B",
            "target_cables_month_12": 20,
            "target_cables_month_18": 40,
            "pricing_port": 50_000,
            "series_a_funding": 15_000_000
        },
        "premium": {
            "name": "Premium/Military Focus",
            "description": "GPU at edge, naval customers, high margins",
            "architecture_option": "A",
            "target_cables_month_12": 10,
            "target_cables_month_18": 15,
            "pricing_naval": 1_000_000,
            "series_a_funding": 20_000_000
        },
        "base_case": {
            "name": "Base Case (From Executive Summary)",
            "description": "Option B strategy as outlined in executive summary",
            "architecture_option": "B",
            "initial_cables": 5,
            "target_cables_month_12": 15,
            "target_cables_month_18": 30,
            "pricing_port": 35_000,
            "pricing_naval": 500_000,
            "series_a_funding": 10_000_000
        }
    }
    return presets


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DAS Monte Carlo Simulator"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
