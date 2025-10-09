# DAS Maritime Surveillance - Monte Carlo Business Simulator

## Overview

This Monte Carlo simulator helps you explore different strategic scenarios for the DAS Maritime Surveillance business. It models uncertainty in customer acquisition, technical performance, costs, and growth to provide probabilistic forecasts of business outcomes.

## What It Does

The simulator models:

### **INPUTS** (What You Control):
- Architecture choice (Option A/B/C)
- Funding amount and cloud credits
- Growth targets (cables deployed over time)
- Pricing by customer segment
- Team size and growth rate
- Simulation parameters

### **STOCHASTIC PARAMETERS** (Uncertainty Modeled):
- Detection accuracy (affected by compression)
- Customer acquisition rate (conversion from leads)
- Customer churn rate
- Cloud costs (variations and negotiations)
- Hardware costs and failure rates
- Salary costs (market variations)
- Deployment timelines (site-specific delays)

### **OUTPUTS** (What You Measure):
- Number of cables deployed over time
- Customers by segment
- Detection accuracy achieved
- Daily detections
- Operational costs (edge, datacenter, cloud, personnel)
- Number of regional datacenters needed
- Team size by role
- Revenue/ARR
- Gross margin
- Cash burn rate and runway
- Time to profitability
- Success probability

## Quick Start

### 1. Install Dependencies

```bash
cd monte_carlo_simulator
pip install -r requirements.txt
```

### 2. Run the Web Service

```bash
python api_service.py
```

Or using uvicorn directly:

```bash
uvicorn api_service:app --reload --host 0.0.0.0 --port 8000
```

### 3. Open the Web Interface

Navigate to: http://localhost:8000

## Using the Simulator

### Web Interface

1. **Choose a Preset** (optional):
   - **Base Case**: Option B strategy from executive summary
   - **Conservative**: Cloud-only, slower growth, lower risk
   - **Aggressive**: Regional datacenter, faster growth
   - **Premium**: GPU at edge, military focus

2. **Adjust Parameters**:
   - **Architecture**: Choose Option A, B, or C
   - **Growth Strategy**: Set cable deployment targets
   - **Pricing**: Adjust monthly prices by customer segment
   - **Team**: Configure initial size and growth rate
   - **Simulation**: Number of Monte Carlo runs (more = slower but more accurate)

3. **Run Simulation**:
   - Click "🚀 Run Simulation"
   - Wait 10-30 seconds (depending on number of simulations)

4. **Analyze Results**:
   - **Success Rate**: Probability of achieving profitability
   - **Series B Qualified**: Probability of hitting $30M ARR milestone
   - **Final Metrics**: Cables, customers, ARR with P10/P50/P90 ranges
   - **Charts**: Revenue, costs, cash, growth trajectories

### API Usage

You can also use the API directly:

```python
import requests

# Configure simulation
config = {
    "architecture_option": "B",
    "series_a_funding": 10000000,
    "target_cables_month_12": 15,
    "target_cables_month_18": 30,
    "pricing_port": 35000,
    "pricing_naval": 500000,
    "num_simulations": 1000,
    "simulation_months": 24
}

# Run simulation
response = requests.post("http://localhost:8000/api/simulate", json=config)
results = response.json()

# Analyze
print(f"Success rate: {results['analysis']['success_metrics']['profitability_rate']:.1%}")
print(f"Median ARR: ${results['analysis']['final_metrics']['arr']['median']/1e6:.1f}M")
```

## Understanding the Results

### Success Metrics

- **Profitability Rate**: % of simulations that achieve positive gross margin (>70%)
- **Series B Qualified Rate**: % that reach $30M ARR with 15+ cables
- **Failure Rate**: % that run out of cash before profitability

### Final Metrics (at Month 18 or 24)

For each output metric, you get:
- **Median (P50)**: Middle outcome - 50% of simulations above/below
- **P10**: Pessimistic outcome - only 10% of simulations worse
- **P90**: Optimistic outcome - only 10% of simulations better

### Charts

- **Revenue & Costs**: Shows P10/P50/P90 trajectories
- **Cash Position**: Critical for runway planning
- **Growth**: Cables deployed and customers acquired
- **Team & Infrastructure**: Scaling requirements
- **Technical Metrics**: Detection accuracy over time

## Key Decision Questions Answered

### 1. Architecture Choice (Option A vs B vs C)

**Question**: Which architecture option provides the best risk-adjusted returns?

**How to use simulator**:
- Run simulations with each architecture option
- Compare success rates and final ARR
- Check failure rates (ran out of cash)

**Example findings**:
- Option C: Lower upfront costs, good for Phase 1
- Option B: Better unit economics at 10+ cables
- Option A: Higher costs, lower success rate unless targeting military

### 2. Growth Strategy

**Question**: How aggressively should we deploy cables?

**How to use simulator**:
- Vary `target_cables_month_12` and `target_cables_month_18`
- Compare cash remaining vs ARR achieved
- Find the sweet spot between growth and runway

**Example findings**:
- Too aggressive (40 cables by M18): 60% run out of cash
- Too conservative (10 cables by M18): Profitable but low ARR, miss Series B
- Optimal (20-30 cables by M18): Balance growth and survival

### 3. Pricing Strategy

**Question**: Can we charge more or should we go lower to acquire faster?

**How to use simulator**:
- Adjust pricing by segment
- See impact on customer acquisition and revenue
- Note: Lower prices don't directly increase conversion in model (you may want to adjust `conversion_rate_port_mean`)

### 4. Team Sizing

**Question**: How many engineers do we need and when?

**How to use simulator**:
- Adjust `initial_team_size` and `team_growth_rate`
- See impact on costs and ability to scale
- Current model assumes team scales with operational needs

### 5. Funding Requirements

**Question**: Is $10M Series A sufficient? When do we need Series B?

**How to use simulator**:
- Vary `series_a_funding`
- Check `cash_remaining` trajectory
- See when `series_b_qualified` becomes true
- Determine ideal Series B timing

## Model Assumptions & Limitations

### Assumptions

1. **Customer acquisition**:
   - Leads scale with cables deployed
   - Conversion rates are stochastic (normal distribution)
   - Sales effectiveness ramps over 12 months

2. **Costs**:
   - Edge infrastructure scales linearly with cables
   - Regional datacenter kicks in at 8 cables (Option B)
   - Cloud costs scale with data volume
   - Team costs based on role distribution

3. **Technical**:
   - Detection accuracy centered at 97% (epsilon=0.1)
   - System uptime ~99.5%
   - Detections per cable ~50/day

4. **Market**:
   - 10% annual price erosion from competition
   - Monthly churn ~2%

### Limitations

1. **No external funding events**: Doesn't model Series B infusion mid-simulation
2. **Simplified customer acquisition**: Doesn't model marketing spend → conversion relationship explicitly
3. **No seasonality**: Customer acquisition and costs are constant
4. **No competition dynamics**: Doesn't model competitive responses
5. **Simplified team model**: Team roles are percentage-based, not optimized for actual needs

### Extending the Model

To add your own stochastic parameters:

```python
# In das_monte_carlo.py, modify StochasticParameters

@dataclass
class StochasticParameters:
    # Add your parameter
    my_new_param_mean: float = 100
    my_new_param_std: float = 10
    
# Then use in simulation
value = np.random.normal(
    self.params.my_new_param_mean,
    self.params.my_new_param_std
)
```

## Advanced Usage

### Running from Command Line

```python
# Run a quick test
python das_monte_carlo.py

# Run custom simulation
from das_monte_carlo import *

inputs = SimulationInputs(
    architecture_option=ArchitectureOption.OPTION_B_REGIONAL_DC,
    target_cables_month_18=40
)
params = StochasticParameters()

simulator = DASMonteCarloSimulator(inputs, params)
results = simulator.run_monte_carlo(num_simulations=5000)

analysis = analyze_results(results)
print(json.dumps(analysis, indent=2))
```

### Exporting Results

```python
# Save trajectories to CSV
import pandas as pd

for i, result in enumerate(results):
    df = pd.DataFrame({
        'month': result.months,
        'cables': result.cables_deployed,
        'revenue': result.revenue_monthly,
        'cash': result.cash_remaining
    })
    df.to_csv(f'simulation_{i}.csv', index=False)
```

## Files

- `das_monte_carlo.py`: Core simulation engine
- `api_service.py`: FastAPI web service wrapper
- `static/index.html`: Web interface
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

Install dependencies: `pip install -r requirements.txt`

### "Address already in use" when starting service

Change port: `uvicorn api_service:app --port 8001`

### Simulation takes too long

Reduce `num_simulations` from 1000 to 100-500 for faster results

### Results don't match executive summary

The Monte Carlo includes uncertainty - executive summary uses deterministic "base case" assumptions. Your results should cluster around executive summary numbers.

## Next Steps

1. **Validate assumptions**: Review `StochasticParameters` and adjust means/stds based on your domain knowledge
2. **Sensitivity analysis**: Run multiple scenarios varying one parameter at a time
3. **Risk analysis**: Focus on scenarios where `ran_out_of_cash` is true - what went wrong?
4. **Decision support**: Use P10/P50/P90 ranges to set realistic targets and communicate uncertainty to board

## Questions?

This simulator is designed to help you answer the questions in `INTERNAL_DECISION_QUESTIONS.md`. For each major decision, run scenarios and compare outcomes.

The goal is not to predict the future exactly, but to:
1. Understand ranges of outcomes
2. Identify key risks
3. Make informed strategic choices
4. Communicate uncertainty to stakeholders
