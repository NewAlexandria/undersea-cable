# Monte Carlo Simulator - Quick Reference Card

## 🎯 What It Does

Simulates 1000+ possible futures for your DAS business to show **probability of success** instead of single forecasts.

---

## 📊 Model Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      YOUR DECISIONS (INPUTS)                      │
├─────────────────────────────────────────────────────────────────┤
│ • Architecture: A/B/C                                            │
│ • Funding: $10M Series A                                         │
│ • Growth: 3→5→15→30 cables                                       │
│ • Pricing: $35k port, $500k naval                                │
│ • Team: Start 5, grow 1.5x per 6mo                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  UNCERTAINTY (STOCHASTIC)                         │
├─────────────────────────────────────────────────────────────────┤
│ • Customer conversion: 15-35% (varies)                           │
│ • Churn: 1-3% monthly                                            │
│ • Detection accuracy: 95-99%                                     │
│ • Costs: ±15% hardware, ±20% salaries                            │
│ • Deployment delays: 1.5-2.5 months                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MONTE CARLO SIMULATION                          │
├─────────────────────────────────────────────────────────────────┤
│ Run 1000 times, each time randomly sampling uncertainty          │
│ Each run: 24 months, month-by-month simulation                   │
│ Track: Cables, customers, revenue, costs, cash, team             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUTS (RESULTS)                            │
├─────────────────────────────────────────────────────────────────┤
│ SUCCESS RATES:                                                    │
│ • 65% achieve profitability                                      │
│ • 55% qualify for Series B                                       │
│ • 20% run out of cash (failure)                                  │
│                                                                   │
│ FINAL METRICS (P10 / P50 / P90):                                 │
│ • Cables: 12 / 30 / 47                                           │
│ • Customers: 45 / 110 / 180                                      │
│ • ARR: $35M / $65M / $95M                                        │
│ • Cash: -$2M / $8M / $25M                                        │
│ • Team: 10 / 18 / 28 people                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 How to Run

### Option 1: Web Interface (Easiest)

```bash
cd /workspace/monte_carlo_simulator
./run_simulator.sh              # Linux/Mac
# or
run_simulator.bat               # Windows
```

Open: http://localhost:8000

### Option 2: API

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "architecture_option": "B",
    "series_a_funding": 10000000,
    "target_cables_month_18": 30,
    "num_simulations": 1000
  }'
```

### Option 3: Python

```python
from das_monte_carlo import *

inputs = SimulationInputs(architecture_option=ArchitectureOption.OPTION_B_REGIONAL_DC)
params = StochasticParameters()
simulator = DASMonteCarloSimulator(inputs, params)
results = simulator.run_monte_carlo(num_simulations=1000)
analysis = analyze_results(results)
```

---

## 📈 Key Outputs Explained

### Success Metrics
- **Profitability Rate**: % of simulations achieving >70% gross margin
- **Series B Qualified**: % reaching $30M ARR with 15+ cables
- **Failure Rate**: % running out of cash before profitability

### Percentiles (P10/P50/P90)
- **P10**: Pessimistic (only 10% worse)
- **P50**: Median/Expected (most likely)
- **P90**: Optimistic (only 10% better)

### Final Metrics
All metrics shown at Month 18 or 24:
- Cables deployed
- Total customers (all segments)
- ARR (Annual Recurring Revenue)
- Cash remaining
- Team size
- Regional datacenters built

---

## 🎯 Strategic Questions Answered

| Question | How to Test | Key Metric |
|----------|-------------|------------|
| **Which architecture?** | Run A vs B vs C | Success rate, median ARR |
| **How fast to grow?** | Vary cable targets | Failure rate, cash remaining |
| **Is $10M enough?** | Vary Series A amount | Failure rate, runway |
| **Team size needed?** | Vary initial team & growth | Team cost %, success rate |
| **When build datacenter?** | Compare B vs C at scale | Infrastructure cost, margin |
| **Pricing strategy?** | Vary port/naval pricing | Revenue, customer count |

---

## ⚙️ Presets Available

### Base Case (Executive Summary)
- Option B (Regional DC)
- $10M Series A
- 5→15→30 cables
- $35k port, $500k naval
- Team: 5 start, 1.5x growth

### Conservative
- Option C (Cloud only)
- Slower growth (10→20 cables)
- Lower pricing ($25k port)
- Risk-averse

### Aggressive
- Option B (Regional DC)
- Faster growth (20→40 cables)
- Higher pricing ($50k port)
- $15M Series A

### Premium/Military
- Option A (GPU at edge)
- Slower growth (10→15 cables)
- $1M naval pricing
- $20M Series A

---

## 🚨 Red Flags to Watch

| Red Flag | Threshold | Action |
|----------|-----------|--------|
| High failure rate | >30% | Reduce growth or increase funding |
| Low success rate | <50% | Adjust strategy significantly |
| P10 cash negative | <$0 | Risk of running out of money |
| Low Series B rate | <40% | May not hit growth milestones |
| Wide P10-P90 range | >3x difference | High uncertainty, plan flexibility |

---

## 📝 Quick Customization

### Change Detection Accuracy
```python
params = StochasticParameters(
    detection_accuracy_mean=0.95,  # 95% instead of 97%
    detection_accuracy_std=0.03
)
```

### Change Customer Conversion
```python
params = StochasticParameters(
    conversion_rate_port_mean=0.30,  # 30% instead of 25%
    conversion_rate_port_std=0.08
)
```

### Add More Simulations
```python
results = simulator.run_monte_carlo(num_simulations=5000)  # More accurate
```

---

## 📁 Files

```
monte_carlo_simulator/
├── das_monte_carlo.py       # Core engine
├── api_service.py           # Web API
├── static/index.html        # Web UI
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
├── QUICK_REFERENCE.md       # This file
├── run_simulator.sh         # Startup script (Linux/Mac)
└── run_simulator.bat        # Startup script (Windows)
```

---

## 💡 Pro Tips

1. **Start with presets**: Load "Base Case" to see executive summary strategy

2. **Run multiple scenarios**: Test at least 3 scenarios before making decisions

3. **Focus on P10**: Worst-case planning prevents disasters

4. **Watch failure rate**: If >20%, strategy is too risky

5. **Increase simulations for important decisions**: 5000-10000 runs for final analysis

6. **Export data**: Save results to CSV for further analysis in Excel/Sheets

7. **Validate assumptions**: Review `StochasticParameters` with domain experts

8. **Iterate**: Adjust inputs based on results, re-run, compare

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Module not found" | Run: `pip install -r requirements.txt` |
| Takes too long | Reduce `num_simulations` to 100-500 |
| Address in use | Change port: `--port 8001` |
| Results look wrong | Check parameter assumptions in code |
| Can't access web UI | Check firewall, try http://127.0.0.1:8000 |

---

## 📞 Support

Documentation:
- Full guide: `README.md`
- Summary: `../MONTE_CARLO_SIMULATOR_SUMMARY.md`
- Decision questions: `../INTERNAL_DECISION_QUESTIONS.md`

---

## Example Results Interpretation

```
✅ SUCCESS: 65% profitability rate, 55% Series B qualified
   → Strategy is viable with acceptable risk

⚠️  WARNING: 20% failure rate
   → 1 in 5 chance of running out of cash
   → Consider: More funding, slower growth, or cost reduction

📊 EXPECTED OUTCOME (P50):
   • 30 cables deployed
   • 110 customers
   • $65M ARR
   • $8M cash remaining
   • 18 team members

🎯 RECOMMENDATION: Proceed with Option B strategy
   Monitor cash closely, prepare for Series B at Month 15-18
```

---

**Last Updated**: Based on executive summary and technical architecture documents
**Version**: 1.0
**Status**: ✅ Production Ready
