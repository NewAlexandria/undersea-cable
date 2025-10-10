"""
DAS Maritime Surveillance Business Monte Carlo Simulator
Simulates business outcomes based on strategic decisions and uncertain parameters
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import json


class ArchitectureOption(Enum):
    """Architecture deployment options"""
    OPTION_A_GPU_EDGE = "A"  # GPU at edge
    OPTION_B_REGIONAL_DC = "B"  # CPU + Regional Datacenter
    OPTION_C_CLOUD_ONLY = "C"  # CPU + Cloud only


class CustomerSegment(Enum):
    """Customer segments with different characteristics"""
    PORT_AUTHORITY = "port"
    NAVAL_MILITARY = "naval"
    ENVIRONMENTAL = "environmental"
    SHIPPING_COMPANY = "shipping"
    INSURANCE = "insurance"


@dataclass
class SimulationInputs:
    """User-controlled inputs to the simulation"""
    # Strategic decisions
    architecture_option: ArchitectureOption = ArchitectureOption.OPTION_C_CLOUD_ONLY
    series_a_funding: float = 10_000_000  # $10M
    compression_error_threshold: float = 0.1  # epsilon for DASPack
    
    # Growth strategy
    initial_cables: int = 3
    target_cables_month_6: int = 5
    target_cables_month_12: int = 15
    target_cables_month_18: int = 30
    
    # Pricing (monthly per cable per customer)
    pricing_port: float = 35_000
    pricing_naval: float = 500_000
    pricing_environmental: float = 10_000
    pricing_shipping: float = 10_000
    pricing_insurance: float = 25_000
    
    # Team strategy
    initial_team_size: int = 5
    team_growth_rate: float = 1.5  # multiply per 6 months
    
    # Cloud strategy
    cloud_provider: str = "GCP"
    cloud_credits_secured: float = 250_000
    
    # Time horizon
    simulation_months: int = 24


@dataclass
class StochasticParameters:
    """Parameters with uncertainty (defined as distributions)"""
    # Detection accuracy (mean, std) by compression level
    detection_accuracy_mean: float = 0.97  # 97% info preserved at epsilon=0.1
    detection_accuracy_std: float = 0.02
    
    # Customer acquisition
    cac_port_mean: float = 50_000  # Customer acquisition cost
    cac_port_std: float = 15_000
    cac_naval_mean: float = 200_000
    cac_naval_std: float = 50_000
    
    conversion_rate_port_mean: float = 0.25  # Lead to customer conversion
    conversion_rate_port_std: float = 0.10
    conversion_rate_naval_mean: float = 0.15
    conversion_rate_naval_std: float = 0.05
    
    churn_rate_monthly_mean: float = 0.02  # 2% monthly churn
    churn_rate_monthly_std: float = 0.01
    
    # Cost variations
    cloud_cost_per_tb_mean: float = 50  # After compression
    cloud_cost_per_tb_std: float = 10
    
    edge_capex_variation: float = 0.15  # +/- 15% from nominal
    salary_variation: float = 0.20  # +/- 20% from target
    
    # Deployment
    cable_deployment_time_months_mean: float = 2.0
    cable_deployment_time_months_std: float = 0.5
    
    # Technical performance
    system_uptime_mean: float = 0.995
    system_uptime_std: float = 0.005
    
    # Market effects
    competitive_pressure_annual: float = 0.10  # 10% annual price reduction pressure


@dataclass
class SimulationOutputs:
    """Outputs tracked over time"""
    months: List[int] = field(default_factory=list)
    
    # Operational metrics
    cables_deployed: List[int] = field(default_factory=list)
    customers_by_segment: List[Dict[str, int]] = field(default_factory=list)
    total_customers: List[int] = field(default_factory=list)
    
    # Technical metrics
    detection_accuracy: List[float] = field(default_factory=list)
    detections_per_day: List[int] = field(default_factory=list)
    system_uptime: List[float] = field(default_factory=list)
    
    # Infrastructure
    regional_datacenters: List[int] = field(default_factory=list)
    
    # Team
    team_size_total: List[int] = field(default_factory=list)
    team_by_role: List[Dict[str, int]] = field(default_factory=list)
    
    # Financial metrics
    revenue_monthly: List[float] = field(default_factory=list)
    costs_monthly: List[float] = field(default_factory=list)
    costs_breakdown: List[Dict[str, float]] = field(default_factory=list)
    gross_margin: List[float] = field(default_factory=list)
    cash_remaining: List[float] = field(default_factory=list)
    arr: List[float] = field(default_factory=list)
    
    # Success metrics
    profitability_achieved: bool = False
    profitability_month: int = None
    series_b_qualified: bool = False
    ran_out_of_cash: bool = False
    failure_month: int = None


class DASMonteCarloSimulator:
    """Monte Carlo simulator for DAS maritime surveillance business"""
    
    def __init__(self, inputs: SimulationInputs, params: StochasticParameters):
        self.inputs = inputs
        self.params = params
        
    def get_architecture_costs(self, arch: ArchitectureOption, num_cables: int) -> Tuple[float, float]:
        """Get capex and monthly opex for architecture choice"""
        if arch == ArchitectureOption.OPTION_A_GPU_EDGE:
            edge_capex_per_cable = 500_000
            edge_opex_monthly = 10_800  # $130k annual / 12
            datacenter_capex = 0
            datacenter_opex_monthly = 0
            cloud_opex_monthly = 4_000 * num_cables  # Minimal cloud use
            
        elif arch == ArchitectureOption.OPTION_B_REGIONAL_DC:
            edge_capex_per_cable = 350_000
            edge_opex_monthly = 2_500  # $30k annual / 12
            # Regional datacenter kicks in at 8+ cables
            datacenter_capex = 2_000_000 if num_cables >= 8 else 0
            datacenter_opex_monthly = 16_700 if num_cables >= 8 else 0  # $200k annual / 12
            cloud_opex_monthly = 4_000 * num_cables  # Storage and backups
            
        else:  # OPTION_C_CLOUD_ONLY
            edge_capex_per_cable = 250_000
            edge_opex_monthly = 2_500  # $30k annual / 12
            datacenter_capex = 0
            datacenter_opex_monthly = 0
            cloud_opex_monthly = 15_000 * num_cables  # $180k annual / 12
        
        # Apply variation
        edge_capex_variation = np.random.normal(1.0, self.params.edge_capex_variation)
        edge_capex_per_cable *= edge_capex_variation
        
        total_opex_monthly = (edge_opex_monthly * num_cables + 
                             datacenter_opex_monthly + 
                             cloud_opex_monthly)
        
        return edge_capex_per_cable, total_opex_monthly
    
    def get_team_costs(self, team_size: int) -> Tuple[float, Dict[str, int]]:
        """Calculate team costs and breakdown by role"""
        # Role distribution (approximate)
        roles = {
            'signal_processing_ml': int(team_size * 0.25),
            'data_engineering': int(team_size * 0.20),
            'cloud_devops': int(team_size * 0.20),
            'edge_hardware': int(team_size * 0.15),
            'product_engineering': int(team_size * 0.20)
        }
        
        # Average salaries by role (annual)
        salaries = {
            'signal_processing_ml': 200_000,
            'data_engineering': 170_000,
            'cloud_devops': 160_000,
            'edge_hardware': 150_000,
            'product_engineering': 165_000
        }
        
        monthly_cost = 0
        for role, count in roles.items():
            salary = salaries[role] * np.random.normal(1.0, self.params.salary_variation)
            monthly_cost += (salary / 12) * count
        
        return monthly_cost, roles
    
    def get_customer_acquisition(self, month: int, cables_deployed: int, 
                                 current_customers: Dict[str, int]) -> Dict[str, int]:
        """Simulate customer acquisition for the month"""
        new_customers = {seg.value: 0 for seg in CustomerSegment}
        
        # Leads available per cable
        leads_per_cable = {
            CustomerSegment.PORT_AUTHORITY: 4,
            CustomerSegment.NAVAL_MILITARY: 1,
            CustomerSegment.ENVIRONMENTAL: 3,
            CustomerSegment.SHIPPING_COMPANY: 2,
            CustomerSegment.INSURANCE: 2
        }
        
        # Conversion rates (stochastic)
        conversion_rates = {
            CustomerSegment.PORT_AUTHORITY: max(0, np.random.normal(
                self.params.conversion_rate_port_mean, 
                self.params.conversion_rate_port_std)),
            CustomerSegment.NAVAL_MILITARY: max(0, np.random.normal(
                self.params.conversion_rate_naval_mean, 
                self.params.conversion_rate_naval_std)),
            CustomerSegment.ENVIRONMENTAL: max(0, np.random.normal(0.30, 0.10)),
            CustomerSegment.SHIPPING_COMPANY: max(0, np.random.normal(0.20, 0.08)),
            CustomerSegment.INSURANCE: max(0, np.random.normal(0.15, 0.08))
        }
        
        # Sales ramp (takes time to build sales team and credibility)
        sales_effectiveness = min(1.0, month / 12)  # Full effectiveness at month 12
        
        for segment in CustomerSegment:
            total_leads = leads_per_cable[segment] * cables_deployed * sales_effectiveness
            conversion = conversion_rates[segment]
            acquired = np.random.binomial(int(total_leads), conversion)
            new_customers[segment.value] = acquired
        
        return new_customers
    
    def apply_churn(self, customers: Dict[str, int]) -> Dict[str, int]:
        """Apply monthly churn to customer base"""
        churn_rate = max(0, min(0.1, np.random.normal(
            self.params.churn_rate_monthly_mean,
            self.params.churn_rate_monthly_std
        )))
        
        churned_customers = {}
        for segment, count in customers.items():
            churned = np.random.binomial(count, churn_rate)
            churned_customers[segment] = max(0, count - churned)
        
        return churned_customers
    
    def calculate_revenue(self, customers: Dict[str, int], month: int) -> float:
        """Calculate monthly revenue from customers"""
        pricing = {
            CustomerSegment.PORT_AUTHORITY.value: self.inputs.pricing_port,
            CustomerSegment.NAVAL_MILITARY.value: self.inputs.pricing_naval,
            CustomerSegment.ENVIRONMENTAL.value: self.inputs.pricing_environmental,
            CustomerSegment.SHIPPING_COMPANY.value: self.inputs.pricing_shipping,
            CustomerSegment.INSURANCE.value: self.inputs.pricing_insurance
        }
        
        # Competitive pressure reduces prices over time
        price_erosion = (1 - self.params.competitive_pressure_annual) ** (month / 12)
        
        revenue = 0
        for segment, count in customers.items():
            revenue += pricing[segment] * count * price_erosion
        
        return revenue
    
    def calculate_detections(self, cables: int, accuracy: float) -> int:
        """Estimate daily vessel detections"""
        # Assume ~50 vessel passages per cable per day on average
        base_detections = cables * 50
        # Accuracy affects successful detections
        detections = int(base_detections * accuracy)
        # Add some random variation
        detections = int(np.random.normal(detections, detections * 0.1))
        return max(0, detections)
    
    def run_single_simulation(self, seed: int = None) -> SimulationOutputs:
        """Run a single Monte Carlo simulation"""
        if seed is not None:
            np.random.seed(seed)
        
        outputs = SimulationOutputs()
        
        # Initial state
        cash = self.inputs.series_a_funding - self.inputs.cloud_credits_secured
        cables_deployed = self.inputs.initial_cables
        customers = {seg.value: 0 for seg in CustomerSegment}
        team_size = self.inputs.initial_team_size
        regional_datacenters = 0
        
        # Cable deployment queue (time it takes to deploy)
        deployment_queue = []
        
        # Initial capex
        edge_capex, _ = self.get_architecture_costs(self.inputs.architecture_option, 1)
        initial_capex = edge_capex * self.inputs.initial_cables
        cash -= initial_capex
        
        for month in range(self.inputs.simulation_months):
            outputs.months.append(month)
            
            # Cable deployment
            # Process deployment queue
            deployed_this_month = []
            for i, (deploy_month, _) in enumerate(deployment_queue):
                if month >= deploy_month:
                    deployed_this_month.append(i)
                    cables_deployed += 1
            for i in reversed(deployed_this_month):
                deployment_queue.pop(i)
            
            # Plan new deployments based on targets
            target_cables = self.inputs.initial_cables
            if month >= 6:
                target_cables = self.inputs.target_cables_month_6
            if month >= 12:
                target_cables = self.inputs.target_cables_month_12
            if month >= 18:
                target_cables = self.inputs.target_cables_month_18
            
            cables_to_deploy = target_cables - cables_deployed - len(deployment_queue)
            if cables_to_deploy > 0:
                for _ in range(cables_to_deploy):
                    deployment_time = np.random.normal(
                        self.params.cable_deployment_time_months_mean,
                        self.params.cable_deployment_time_months_std
                    )
                    deploy_month = month + int(deployment_time)
                    edge_capex_per_cable, _ = self.get_architecture_costs(
                        self.inputs.architecture_option, 1)
                    deployment_queue.append((deploy_month, edge_capex_per_cable))
                    cash -= edge_capex_per_cable  # Pay upfront
            
            # Regional datacenter decision (Option B, >8 cables)
            if (self.inputs.architecture_option == ArchitectureOption.OPTION_B_REGIONAL_DC 
                and cables_deployed >= 8 and regional_datacenters == 0):
                regional_datacenters = 1
                cash -= 2_000_000  # Datacenter capex
            
            # Customer acquisition
            new_customers = self.get_customer_acquisition(month, cables_deployed, customers)
            for segment, count in new_customers.items():
                customers[segment] = customers.get(segment, 0) + count
            
            # Apply churn
            customers = self.apply_churn(customers)
            
            # Calculate revenue
            revenue = self.calculate_revenue(customers, month)
            
            # Calculate costs
            _, infra_opex = self.get_architecture_costs(
                self.inputs.architecture_option, cables_deployed)
            team_cost, team_breakdown = self.get_team_costs(team_size)
            
            # Marketing/Sales costs (estimate)
            sales_marketing_cost = 50_000 + (5_000 * team_size)  # Scales with team
            
            # Support/Operations (estimate)
            support_cost = 10_000 * cables_deployed * 0.05  # 5% of cable value
            
            total_costs = infra_opex + team_cost + sales_marketing_cost + support_cost
            
            costs_breakdown = {
                'infrastructure': infra_opex,
                'personnel': team_cost,
                'sales_marketing': sales_marketing_cost,
                'support': support_cost
            }
            
            # Update cash
            cash += revenue - total_costs
            
            # Technical metrics
            detection_accuracy = np.random.normal(
                self.params.detection_accuracy_mean,
                self.params.detection_accuracy_std
            )
            detection_accuracy = max(0.8, min(1.0, detection_accuracy))
            
            system_uptime = np.random.normal(
                self.params.system_uptime_mean,
                self.params.system_uptime_std
            )
            system_uptime = max(0.9, min(1.0, system_uptime))
            
            detections = self.calculate_detections(cables_deployed, detection_accuracy)
            
            # Team growth
            if month > 0 and month % 6 == 0:
                team_size = int(team_size * self.inputs.team_growth_rate)
            
            # Record outputs
            outputs.cables_deployed.append(cables_deployed)
            outputs.customers_by_segment.append(dict(customers))
            outputs.total_customers.append(sum(customers.values()))
            outputs.detection_accuracy.append(detection_accuracy)
            outputs.detections_per_day.append(detections)
            outputs.system_uptime.append(system_uptime)
            outputs.regional_datacenters.append(regional_datacenters)
            outputs.team_size_total.append(team_size)
            outputs.team_by_role.append(team_breakdown)
            outputs.revenue_monthly.append(revenue)
            outputs.costs_monthly.append(total_costs)
            outputs.costs_breakdown.append(costs_breakdown)
            
            gross_margin = (revenue - total_costs) / revenue if revenue > 0 else -1
            outputs.gross_margin.append(gross_margin)
            outputs.cash_remaining.append(cash)
            outputs.arr.append(revenue * 12)
            
            # Check for profitability
            if not outputs.profitability_achieved and gross_margin > 0.7 and revenue > total_costs:
                outputs.profitability_achieved = True
                outputs.profitability_month = month
            
            # Check for Series B qualification (example criteria)
            if (revenue * 12 > 30_000_000 and  # $30M ARR
                gross_margin > 0.6 and
                cables_deployed >= 15):
                outputs.series_b_qualified = True
            
            # Check for failure (ran out of cash)
            if cash < 0:
                outputs.ran_out_of_cash = True
                outputs.failure_month = month
                break
        
        return outputs
    
    def run_monte_carlo(self, num_simulations: int = 1000) -> List[SimulationOutputs]:
        """Run Monte Carlo simulation with multiple iterations"""
        results = []
        for i in range(num_simulations):
            outputs = self.run_single_simulation(seed=i)
            results.append(outputs)
        return results


def analyze_results(results: List[SimulationOutputs]) -> Dict:
    """Analyze Monte Carlo results and return summary statistics"""
    num_sims = len(results)
    
    # Success rates
    profitability_rate = sum(1 for r in results if r.profitability_achieved) / num_sims
    series_b_qualified_rate = sum(1 for r in results if r.series_b_qualified) / num_sims
    failure_rate = sum(1 for r in results if r.ran_out_of_cash) / num_sims
    
    # Time to profitability
    profitable_sims = [r for r in results if r.profitability_achieved]
    avg_months_to_profit = (sum(r.profitability_month for r in profitable_sims) / 
                           len(profitable_sims)) if profitable_sims else None
    
    # Final metrics (month 18 or last month)
    final_cables = [r.cables_deployed[-1] for r in results if len(r.cables_deployed) > 0]
    final_customers = [r.total_customers[-1] for r in results if len(r.total_customers) > 0]
    final_arr = [r.arr[-1] for r in results if len(r.arr) > 0]
    final_cash = [r.cash_remaining[-1] for r in results if len(r.cash_remaining) > 0]
    final_team = [r.team_size_total[-1] for r in results if len(r.team_size_total) > 0]
    
    analysis = {
        'num_simulations': num_sims,
        'success_metrics': {
            'profitability_rate': profitability_rate,
            'series_b_qualified_rate': series_b_qualified_rate,
            'failure_rate': failure_rate,
            'avg_months_to_profitability': avg_months_to_profit
        },
        'final_metrics': {
            'cables_deployed': {
                'mean': np.mean(final_cables),
                'median': np.median(final_cables),
                'p10': np.percentile(final_cables, 10),
                'p90': np.percentile(final_cables, 90)
            },
            'total_customers': {
                'mean': np.mean(final_customers),
                'median': np.median(final_customers),
                'p10': np.percentile(final_customers, 10),
                'p90': np.percentile(final_customers, 90)
            },
            'arr': {
                'mean': np.mean(final_arr),
                'median': np.median(final_arr),
                'p10': np.percentile(final_arr, 10),
                'p90': np.percentile(final_arr, 90)
            },
            'cash_remaining': {
                'mean': np.mean(final_cash),
                'median': np.median(final_cash),
                'p10': np.percentile(final_cash, 10),
                'p90': np.percentile(final_cash, 90)
            },
            'team_size': {
                'mean': np.mean(final_team),
                'median': np.median(final_team),
                'p10': np.percentile(final_team, 10),
                'p90': np.percentile(final_team, 90)
            }
        }
    }
    
    return analysis


if __name__ == "__main__":
    # Example usage
    inputs = SimulationInputs()
    params = StochasticParameters()
    
    simulator = DASMonteCarloSimulator(inputs, params)
    
    print("Running single simulation...")
    result = simulator.run_single_simulation(seed=42)
    print(f"Final month: {result.months[-1]}")
    print(f"Cables deployed: {result.cables_deployed[-1]}")
    print(f"Total customers: {result.total_customers[-1]}")
    print(f"ARR: ${result.arr[-1]:,.0f}")
    print(f"Cash remaining: ${result.cash_remaining[-1]:,.0f}")
    print(f"Profitability achieved: {result.profitability_achieved}")
