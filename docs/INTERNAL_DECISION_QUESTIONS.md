---
layout: default
title: "Internal Decision Questions for Milestone Planning"
description: "Strategic questions to answer internally for defining milestones in technical validation, architectural scale, and partner engagement with focus on team resourcing and cost metrics."
---

# Internal Decision Questions for Milestone Planning

## Purpose

This document contains critical questions **you need to answer internally** to set concrete milestones and targets for:

1. **Technical Validation** - What do we need to prove technically?
2. **Architectural Scale** - When and how do we scale infrastructure?
3. **Partner Engagement** - Who do we engage and when?

Special focus on:

- Team size and resourcing for multi-cloud services design
- Dashboards/metrics for platform costs
- Multi-vendor comparisons

---

## Section 1: Technical Validation Milestones

### 1.1 Compression Fidelity Validation

**Questions to Answer:**

1. **What specific vessel detection accuracy degradation is acceptable?**

   - Is 97% preservation of vessel information (2.9/3.0 bits) sufficient for our primary use cases?
   - At what accuracy threshold would customers reject the product? (99.9%, 99.5%, 99%, 95%?)
   - Do different customer segments have different accuracy requirements?

2. **What compression error thresholds need validation?**

   - Current plan: ε=0.1 (low loss), ε=0.5 (high loss)
   - Do we need to validate: ε=0.05, 0.1, 0.2, 0.5, 1.0?
   - How many real-world datasets are needed to validate each threshold?
   - Timeline: How long to acquire and validate each dataset?

3. **What vessel types/scenarios MUST be validated before launch?**
   - Large cargo ships (>10k tons): Required for MVP?
   - Medium vessels (1-10k tons): Required for MVP?
   - Small vessels (<1k tons): Required for MVP?
   - Submarines: Required for MVP or Phase 2?
   - Overlapping vessels: Required validation?
   - Adverse weather/high sea state: Required validation?

**Milestone Definition Needed:**

- [ ] Define minimum dataset size for validation (X hours of data, Y vessel passages)
- [ ] Define acceptance criteria: "99.X% accuracy on Z vessel types with ε=W compression"
- [ ] Set timeline: Complete validation by [DATE]
- [ ] Budget: Allocate \$XXk for data acquisition and validation compute

### 1.2 Latency Requirements Validation

**Questions to Answer:**

1. **What latency is acceptable for each customer segment?**

   - Ports: <1s, <3s, <10s, or <30s acceptable?
   - Coast Guard: <1s, <3s, or <10s?
   - Environmental agencies: Minutes acceptable?
   - Research institutions: Hours acceptable?

2. **Can we validate latency acceptance with lighthouse customers before committing to architecture?**

   - Approach: Deploy Option C (cloud, 5-30s latency) for pilots
   - Get customer feedback on whether they'd pay MORE for <3s (Option B) or <1s (Option A)
   - Milestone: "3 lighthouse customers confirm latency requirements by [DATE]"

3. **What's the network latency budget breakdown?**
   - Edge to regional datacenter: Target X ms
   - Regional datacenter processing: Target Y ms
   - Datacenter to cloud: Target Z ms
   - End-to-end acceptable: <3000 ms total?
   - Milestone: "Network latency validated on 3 geographic routes by [DATE]"

**Milestone Definition Needed:**

- [ ] Complete customer interviews on latency requirements by [DATE]
- [ ] Document latency requirements per customer segment in product spec
- [ ] Validate network paths achieve <Xms edge-to-datacenter on Y routes by [DATE]

### 1.3 Multi-Cable Correlation Validation

**Questions to Answer:**

1. **At what scale do we need multi-cable correlation working?**

   - MVP (5 cables): Single-cable detection sufficient?
   - Phase 2 (15 cables): Multi-cable correlation required?
   - Phase 3 (30 cables): Full vessel tracking across network?

2. **What vessel tracking accuracy is required?**

   - Position estimation: Within X meters/kilometers?
   - Velocity estimation: Within Y knots?
   - Vessel ID consistency: Z% of time same vessel identified across cables?

3. **What's the time synchronization requirement?**
   - GPS-disciplined oscillators at each site: Required by MVP?
   - Time sync accuracy: <1ms, <10ms, <100ms?
   - Budget: \$Xk per site for time sync hardware

**Milestone Definition Needed:**

- [ ] Define multi-cable correlation requirements by Phase (1, 2, 3)
- [ ] Validate time synchronization approach on 2 cable sites by [DATE]
- [ ] Achieve X% vessel tracking accuracy across Y cables by [DATE]

---

## Section 2: Architectural Scale Milestones

### 2.1 Architecture Decision Timeline

**Critical Questions:**

1. **When do we COMMIT to Option B (CPU + Regional DC) vs Option C (CPU + Cloud)?**

   - Trigger: After X customer pilots?
   - Trigger: After Y cables deployed?
   - Trigger: After validating Z technical metrics?
   - Timeline: Decide by [DATE] to allow for datacenter buildout

2. **What's the decision criteria for building first regional datacenter?**

   - Number of cables: 8, 10, or 15 cables?
   - Geographic density: X cables within Y km radius?
   - Customer contracts: \$Z ARR committed?
   - Timeline: Decision point at Month X, operational by Month Y

3. **Do we build, colocate, or lease datacenter infrastructure?**
   - Build: \$2M capex, 6-month timeline, full control
   - Colocate: $500k setup + $200k/year, 3-month timeline, less control
   - Lease GPU cloud: \$XXk/month, immediate, operational flexibility
   - Decision needed by: [DATE]

**Milestone Definition Needed:**

- [ ] Set decision trigger: "Choose Option B vs C by [DATE] or [X cables] or [$Y ARR]"
- [ ] Evaluate 3 datacenter locations (US/EU/APAC) by [DATE]
- [ ] Complete build vs colocate vs lease analysis by [DATE]
- [ ] Budget: Reserve \$2M for potential datacenter if triggered

### 2.2 Edge Infrastructure Scaling

**Questions to Answer:**

1. **What's our edge deployment capacity?**

   - Current capability: X cables per quarter
   - Target capability: Y cables per quarter by Q[X]
   - Bottleneck: Hardware procurement, installation teams, or site negotiations?
   - Resource needed: Z installation teams, W site engineers

2. **Do we standardize on single edge hardware config or multiple?**

   - Single config: \$350k CPU-only for all sites (simpler ops)
   - Multi-tier: $500k GPU for Tier 1, $350k CPU for Tier 2 (complex ops)
   - Decision criteria: Customer requirements, or operational simplicity?

3. **What's our edge hardware refresh strategy?**
   - Lifetime: 5 years, 7 years, or 10 years?
   - Upgrade path: Replace CPUs, add GPUs, or swap entire system?
   - Budget: \$XXk per site per year for hardware refresh

**Milestone Definition Needed:**

- [ ] Define standard edge hardware BOM by [DATE]
- [ ] Negotiate hardware agreements with X vendors by [DATE]
- [ ] Build installation team capacity to Y cables/quarter by Q[X]
- [ ] Establish installation playbook and deployment timeline (<30 days per site)

### 2.3 Cloud/Multi-Cloud Strategy

**Questions to Answer:**

1. **Single cloud or multi-cloud from Day 1?**

   - Single (GCP/AWS/Azure): Faster MVP, vendor lock-in risk
   - Multi-cloud: Slower development, better negotiating position
   - Hybrid: Core on one cloud, DR/overflow on second?

2. **What cloud services are we committed to vs abstracted?**

   - Kubernetes: Portable across clouds (use)
   - Managed databases: Cloud-specific (abstract with ORM or accept lock-in?)
   - Object storage: Portable (S3 API standard)
   - ML platforms: Cloud-specific (Vertex AI vs SageMaker vs Azure ML - commit or abstract?)

3. **What's our cloud cost budget by phase?**

   - Phase 1 (3-5 cables): \$Xk/month acceptable?
   - Phase 2 (15 cables): \$Yk/month acceptable?
   - Phase 3 (30 cables): \$Zk/month acceptable?
   - Trigger: Build regional datacenter if cloud costs exceed \$X/month?

4. **What cloud regions are required?**
   - US: us-west-2 (Oregon), us-east-1 (Virginia)?
   - EU: eu-central-1 (Frankfurt)?
   - APAC: asia-northeast-1 (Tokyo)?
   - Latency requirement: <50ms edge-to-region for X% of sites?

**Milestone Definition Needed:**

- [ ] Choose primary cloud provider by [DATE](GCP/AWS/Azure)
- [ ] Complete multi-cloud feasibility study by [DATE]
- [ ] Negotiate cloud credits/discounts: Target \$Xk credits by [DATE]
- [ ] Define cloud cost budget by phase and set up cost monitoring
- [ ] Set trigger: "Move to regional datacenter if cloud compute >\$X/month for Y months"

---

## Section 3: Partner Engagement Strategy

### 3.1 Cable Operator Partnerships

**Questions to Answer:**

1. **What's our cable operator engagement priority?**

   - Rank by: Geographic coverage, customer access, or technical capability?
   - Top 3 targets: SubCom, Alcatel, NEC, or others?
   - Engagement model: Revenue share (20%?), licensing fee, or joint venture?

2. **What do we need FROM cable operators?**

   - Access to cable landing stations (site space, power, network)
   - Introductions to cable customers (ports, telecom, government)
   - Technical support (fiber specs, interrogator integration)
   - Co-marketing (joint go-to-market)

3. **What milestones trigger cable operator engagement?**
   - Trigger 1: After technical validation complete (Month X)?
   - Trigger 2: After first lighthouse customer signed?
   - Trigger 3: After Series A funding secured?

**Milestone Definition Needed:**

- [ ] Rank top 5 cable operators by priority by [DATE]
- [ ] Prepare partnership proposal (revenue share %, term sheet) by [DATE]
- [ ] Secure first cable operator MOU/partnership by [DATE]
- [ ] Target: X cable operator partnerships by end of Year 1

### 3.2 Cloud Provider Partnerships

**Questions to Answer:**

1. **What's our ask from cloud providers?**

   - Cloud credits: $Xk in startup credits (typical: $100k-\$500k)
   - Technical support: Dedicated solutions architect?
   - Co-selling: Introduction to maritime/government customers?
   - Technology access: Early access to GPUs, TPUs, edge compute?

2. **Which cloud provider offers best strategic value?**

   - GCP: Strong ML/AI, submarine cable operator, Google engineer connection
   - AWS: Dominant market share, GovCloud for military customers
   - Azure: Government relationships, hybrid cloud capabilities
   - Scoring criteria: Credits, technical fit, customer access, strategic alignment

3. **What milestones unlock cloud partnership benefits?**
   - Startup credits: Application process, requires [X documentation]
   - Solutions architect: Requires \$Xk/month spend commitment?
   - Co-selling: Requires customer case study or [Y] validation?

**Milestone Definition Needed:**

- [ ] Apply for GCP/AWS/Azure startup programs by [DATE]
- [ ] Secure \$Xk cloud credits commitment by [DATE]
- [ ] Meet with cloud provider enterprise sales by [DATE]
- [ ] Negotiate volume discounts (target: X% off list price at Y scale) by [DATE]

### 3.3 System Integrator Partnerships

**Questions to Answer:**

1. **When do we need system integrator (SI) partnerships?**

   - For government/military sales: Required immediately or Phase 2?
   - For large port authorities: Required immediately or can sell direct?
   - For international expansion: Required for which geographies?

2. **Which SIs are priority partners?**

   - Defense: Lockheed Martin, Raytheon, Northrop Grumman, Thales
   - Maritime: Kongsberg, Wartsila, others?
   - IT/Cloud: Accenture, Deloitte, others?
   - Selection criteria: Customer access, technical capability, partnership terms

3. **What partnership model?**
   - Reseller: SI sells our product (X% margin)
   - Referral: SI introduces customers (Y% referral fee)
   - Co-development: SI integrates our product into their solutions (revenue share)
   - OEM: SI white-labels our technology (licensing model)

**Milestone Definition Needed:**

- [ ] Identify top 3 SI partners per segment (defense, maritime, IT) by [DATE]
- [ ] Prepare SI partnership proposal and pricing by [DATE]
- [ ] Sign first SI partnership agreement by [DATE]
- [ ] Target: X SI partnerships by end of Year 1

### 3.4 Technology/Research Partnerships

**Questions to Answer:**

1. **Do we need academic/research partnerships?**

   - For: Algorithm validation, publications, credibility
   - Against: Slower, IP concerns, resource intensive
   - Candidates: MIT, Stanford, NOAA, Naval Postgraduate School?

2. **What do we need from research partners?**

   - Access to datasets for ML training
   - Algorithm validation and peer review
   - Student interns/recruiting pipeline
   - Publications for credibility

3. **What milestones justify research partnerships?**
   - Phase 1: Focus on product, no bandwidth for research?
   - Phase 2: Once product proven, invest in advanced R&D?
   - Continuous: Academic advisory board from Day 1?

**Milestone Definition Needed:**

- [ ] Decide on research partnership strategy (yes/no/later) by [DATE]
- [ ] If yes: Identify top 3 research partners and engagement model by [DATE]
- [ ] Establish academic advisory board (X professors) by [DATE]

---

## Section 4: Team Size & Resourcing

### 4.1 Multi-Cloud Services Design Team

**Critical Questions:**

1. **What team size is required for multi-cloud platform development?**

   - Platform architecture: X cloud architects
   - DevOps/SRE: Y engineers for infrastructure-as-code, CI/CD
   - Security: Z engineers for multi-cloud security, compliance
   - Total team: X + Y + Z = ? engineers

2. **What skills are required for multi-cloud expertise?**

   - Must have: Kubernetes, Terraform, Docker, CI/CD
   - Cloud-specific: GCP/AWS/Azure certifications
   - Specialized: Multi-cloud networking, security, cost optimization
   - Seniority: Senior (5+ years) vs mid-level (2-5 years) ratio?

3. **Build vs hire vs outsource for multi-cloud team?**

   - Build internal team: X FTEs at $Y salary = $Z annual cost
   - Hire consultancy: $X per hour, Y hours = $Z project cost
   - Hybrid: Core internal team + consultants for peaks
   - Decision criteria: Time to market, cost, long-term capability

4. **What's the team ramp schedule?**
   - Month 0-3: X engineers (core platform)
   - Month 3-6: Y engineers (add ML platform)
   - Month 6-12: Z engineers (scale operations)
   - Year 2: W engineers (multi-region expansion)

**Milestone Definition Needed:**

- [ ] Define multi-cloud platform team structure by [DATE]
- [ ] Budget: Allocate $Xk for Year 1 salaries ($150k-\$200k per engineer)
- [ ] Create job descriptions and begin recruiting by [DATE]
- [ ] Target: Hire X engineers by [QUARTER], Y engineers by [QUARTER]
- [ ] Decide build vs hire vs outsource strategy by [DATE]

### 4.2 Edge/Hardware Team

**Questions to Answer:**

1. **What team is required for edge infrastructure at scale?**

   - Hardware design/procurement: X engineers
   - Installation/deployment: Y field engineers
   - Support/maintenance: Z remote support engineers
   - Total team: X + Y + Z = ? engineers
   - Scaling: Team size at 5 cables, 15 cables, 30 cables?

2. **How many installation teams do we need?**

   - Installation time per site: X days
   - Target deployment rate: Y cables per quarter
   - Required teams: Z teams (assume 1 team = 2-3 engineers)
   - Team cost: \$Xk per team per year

3. **Build internal installation teams vs contractors?**
   - Internal: Higher quality, slower ramp, higher fixed cost
   - Contractors: Faster ramp, variable cost, less control
   - Hybrid: Internal project managers + contractor labor?

**Milestone Definition Needed:**

- [ ] Define edge team structure and size by [DATE]
- [ ] Budget: $Xk for edge team Year 1 (Y engineers at $Z salary)
- [ ] Recruit/train first installation team by [DATE]
- [ ] Complete X successful installations as validation by [DATE]
- [ ] Scale to Y installation teams by [QUARTER] to support Z cables/quarter

### 4.3 Signal Processing & ML Team

**Questions to Answer:**

1. **What team size for core algorithms?**

   - Signal processing (FFT, compression): X PhDs/experts
   - ML/classification: Y ML engineers
   - Computer vision (if applicable): Z engineers
   - Total: X + Y + Z = ? engineers
   - Timeline: Build team by Month X to support launch

2. **What seniority/expertise is required?**

   - Senior/Staff level (PhD or 10+ years): X engineers
   - Mid-level (3-5 years): Y engineers
   - Junior (0-2 years): Z engineers
   - Specific expertise: Acoustic signal processing, marine acoustic classification

3. **External advisors vs internal team?**
   - Core algorithms: Must be internal (IP ownership)
   - Domain expertise: Advisors acceptable (marine acoustics, oceanography)
   - Consulting model: $X per hour for Y hours = $Z budget

**Milestone Definition Needed:**

- [ ] Define signal processing/ML team structure by [DATE]
- [ ] Budget: $Xk for Year 1 ($180k-\$250k per senior engineer)
- [ ] Recruit Head of Signal Processing/ML by [DATE]
- [ ] Hire X engineers by [QUARTER], Y engineers by [QUARTER]
- [ ] Establish advisor network (X advisors, Y domains) by [DATE]

### 4.4 Data Engineering Team

**Questions to Answer:**

1. **What data team size is required?**

   - Streaming data engineering: X engineers (Kafka, Kinesis, real-time)
   - Batch data engineering: Y engineers (Spark, data lake, ETL)
   - Data infrastructure: Z engineers (databases, storage, pipelines)
   - Total: X + Y + Z = ? engineers

2. **What's the data team ramp?**

   - Phase 1 (single cable): X engineers sufficient
   - Phase 2 (10 cables): Y engineers required
   - Phase 3 (30 cables): Z engineers required
   - Scaling trigger: Add engineer per X cables?

3. **What data roles are critical vs nice-to-have?**
   - Critical (must have for MVP): Data pipeline engineer, infrastructure engineer
   - Important (Phase 2): Data scientist, analytics engineer
   - Nice-to-have (Phase 3): ML platform engineer, data governance

**Milestone Definition Needed:**

- [ ] Define data team structure by [DATE]
- [ ] Budget: $Xk for Year 1 ($150k-\$180k per engineer)
- [ ] Hire first data engineers (X engineers) by [DATE]
- [ ] Build MVP data pipeline by [DATE]
- [ ] Scale team to Y engineers by [QUARTER]

### 4.5 Overall Team Budget

**Questions to Answer:**

1. **What's the total engineering team size and cost?**

   - Year 1: X engineers at average $Y salary = $Z total
   - Year 2: X engineers at average $Y salary = $Z total
   - Year 3: X engineers at average $Y salary = $Z total

2. **What's the engineering vs non-engineering split?**

   - Engineering (product, platform, ML): X% of team
   - Sales & Marketing: Y% of team
   - Operations: Z% of team
   - Executive & Admin: W% of team

3. **Does our Series A funding support this team?**
   - Series A: \$10M total
   - Engineering budget (30%): \$3M for 18 months
   - Salaries: $3M / 18 months = $167k/month = ~15-20 engineers average
   - Is this sufficient for: Multi-cloud (3), edge (4), ML (4), data (3), product (3) = 17 engineers?

**Milestone Definition Needed:**

- [ ] Complete detailed team budget model by [DATE]
- [ ] Validate team size fits Series A budget by [DATE]
- [ ] Set team size milestones: X engineers by Month 6, Y by Month 12, Z by Month 18
- [ ] Define hiring priority: Role 1, Role 2, Role 3, ... Role N

---

## Section 5: Cost Metrics & Dashboards

### 5.1 Platform Cost Metrics

**Critical Questions:**

1. **What cost metrics do we track?**

   - Cost per cable per month: Target \$X
   - Cost per TB processed: Target \$Y
   - Cost per vessel detection: Target \$Z
   - Cost per customer per month: Target \$W
   - Gross margin per cable: Target X%

2. **What's the cost breakdown structure?**

   ```
   Total Cost per Cable
   ├── Edge Infrastructure
   │   ├── Hardware (amortized): $X/month
   │   ├── Power & Cooling: $Y/month
   │   ├── Bandwidth: $Z/month
   │   └── Maintenance: $W/month
   ├── Cloud/Datacenter Compute
   │   ├── FFT Processing: $X/month
   │   ├── ML Inference: $Y/month
   │   ├── Data Storage: $Z/month
   │   └── Network egress: $W/month
   ├── Personnel (allocated)
   │   ├── Engineering (amortized): $X/month
   │   ├── Support: $Y/month
   │   └── Operations: $Z/month
   └── Total: $XX,XXX/month
   ```

3. **What are our cost targets by phase?**

   - Phase 1 (5 cables): Total cost $X/month, cost per cable $Y
   - Phase 2 (15 cables): Total cost $X/month, cost per cable $Y (20% reduction)
   - Phase 3 (30 cables): Total cost $X/month, cost per cable $Y (40% reduction)
   - Economies of scale: X% cost reduction per doubling of cables

4. **What's our gross margin target?**
   - Year 1: X% (acceptable due to fixed cost scaling)
   - Year 2: Y% (target 60%?)
   - Year 3: Z% (target 70%?)
   - Competitive benchmark: What margin do Spire Maritime, exactEarth have?

**Milestone Definition Needed:**

- [ ] Define cost metrics and targets by [DATE]
- [ ] Build cost tracking spreadsheet/dashboard by [DATE]
- [ ] Set cost reduction targets: X% per quarter, Y% per year
- [ ] Achieve cost per cable <\$X by [QUARTER]
- [ ] Achieve gross margin >X% by [QUARTER]

### 5.2 Cost Dashboard Requirements

**Questions to Answer:**

1. **What cost dashboards do we need?**

   - Executive dashboard: Total cost, cost per cable, gross margin (monthly)
   - Engineering dashboard: Cloud costs by service, compute utilization (daily)
   - Operations dashboard: Edge costs, bandwidth usage, outages (real-time)
   - Finance dashboard: P&L by customer segment, unit economics (monthly)

2. **What drill-down capabilities are required?**

   - Total cost → By cable → By infrastructure component → By cloud service
   - By time: Month, week, day, hour
   - By geography: US, EU, APAC
   - By customer type: Port, naval, environmental

3. **What alerting do we need on cost metrics?**

   - Alert: Cloud costs exceed \$X/day for Y consecutive days
   - Alert: Cost per cable increases >X% month-over-month
   - Alert: Gross margin falls below X%
   - Alert: Specific service costs spike >X% from baseline

4. **What tools do we use for cost tracking?**
   - Cloud-native: GCP Cost Management, AWS Cost Explorer, Azure Cost Management
   - Third-party: Kubecost, CloudHealth, Datadog
   - Custom: Build internal dashboard (Grafana, Tableau, etc.)
   - Decision criteria: Integration, granularity, cost of tool itself

**Milestone Definition Needed:**

- [ ] Define cost dashboard requirements by [DATE]
- [ ] Choose cost tracking tools by [DATE]
- [ ] Implement MVP cost dashboard by [DATE]
- [ ] Train team on cost monitoring by [DATE]
- [ ] Establish weekly cost review meeting by [DATE]

### 5.3 Multi-Vendor Cost Comparison

**Questions to Answer:**

1. **What vendors do we need to compare?**

   - Cloud compute: GCP vs AWS vs Azure (GPU costs)
   - Cloud storage: GCP Cloud Storage vs AWS S3 vs Azure Blob
   - Managed services: GKE vs EKS vs AKS (Kubernetes)
   - Networking: Cloud interconnect vs dedicated fiber vs SD-WAN
   - Edge hardware: NVIDIA vs AMD GPUs, Intel vs AMD CPUs

2. **What's our cost comparison methodology?**

   - Baseline workload definition: X TB/day processing, Y GPU hours, Z TB storage
   - Vendor quotes: List price, negotiated discount, volume commitments
   - TCO analysis: 1 year, 3 years, 5 years
   - Include: Setup costs, migration costs, operational complexity

3. **When do we trigger multi-vendor RFP?**

   - Trigger 1: At \$X/month spend (negotiate better rates)
   - Trigger 2: Annual contract renewal
   - Trigger 3: Before committing to regional datacenter
   - Timeline: Run RFP process every X months

4. **What's our multi-cloud strategy for cost optimization?**
   - Single cloud with annual negotiations (simpler)
   - Multi-cloud for cost arbitrage (more complex, operational overhead)
   - Hybrid: Primary cloud + backup for DR and price negotiation leverage
   - Decision: Single vs multi-cloud by [DATE]

**Milestone Definition Needed:**

- [ ] Define vendor comparison framework by [DATE]
- [ ] Run initial RFP for cloud providers by [DATE]
- [ ] Negotiate X% discount off list prices by [DATE]
- [ ] Establish annual RFP process for major vendors
- [ ] Document vendor switching costs (prevents lock-in) by [DATE]

### 5.4 Cost Optimization Strategy

**Questions to Answer:**

1. **What are our top cost optimization opportunities?**

   - Compute: Spot instances (AWS/GCP/Azure) save X%, acceptable for batch jobs?
   - Storage: Tiered storage (hot/warm/cold) saves Y%, retention policy defined?
   - Networking: Reduce egress costs by Z%, use private links/colocation?
   - Compression: Higher compression ratios save W% storage, acceptable quality loss?

2. **What cost optimization timeline?**

   - Phase 1: Accept higher costs for speed (move fast)
   - Phase 2: Optimize obvious inefficiencies (low-hanging fruit)
   - Phase 3: Deep optimization for profitability (after product-market fit)
   - Milestones: Achieve X% cost reduction in Phase 2, Y% in Phase 3

3. **What's the trade-off between cost and complexity?**

   - Example: Multi-cloud saves X% but adds Y engineering overhead
   - Example: Spot instances save X% but add Z reliability complexity
   - Decision framework: Optimize if savings > \$X/month OR >Y% improvement

4. **What cost controls do we put in place?**
   - Budget limits: Cloud spending capped at \$X/month, alerts at 80%
   - Approval process: Spending >\$Y requires approval
   - Resource tagging: All cloud resources tagged (cable_id, environment, team)
   - Regular reviews: Weekly cost review, monthly optimization sprint

**Milestone Definition Needed:**

- [ ] Identify top 5 cost optimization opportunities by [DATE]
- [ ] Implement cost controls (budgets, approvals, tagging) by [DATE]
- [ ] Achieve X% cost reduction through optimization by [QUARTER]
- [ ] Establish cost optimization culture (monthly review, team targets) by [DATE]

---

## Section 6: Success Criteria & Checkpoints

### 6.1 Technical Validation Success Criteria

**Define by Phase:**

**Phase 1 (Months 0-6): Proof of Concept**

- [ ] Compression validation: X% vessel information preserved at ε=0.1
- [ ] Detection accuracy: Y% on Z vessel types
- [ ] Latency: <W seconds end-to-end
- [ ] System uptime: >X% over Y day period

**Phase 2 (Months 6-12): Pilot Deployment**

- [ ] Multi-cable correlation: X% tracking accuracy across Y cables
- [ ] Customer validation: Z lighthouse customers confirm value
- [ ] Scalability: Process data from X cables simultaneously
- [ ] Cost: Achieve <\$Y cost per cable per month

**Phase 3 (Months 12-18): Scale & Refine**

- [ ] Architecture decision: Commit to Option B or C based on validation
- [ ] Team scale: X engineers hired and productive
- [ ] Customer scale: Y paid customers, \$Z ARR
- [ ] Infrastructure scale: W cables deployed and operational

### 6.2 Go/No-Go Decision Points

**Decision Point 1: Proceed to Series A (Month 3)**

- Go if: Technical validation complete, 2+ LOIs from customers
- No-go if: Detection accuracy <X%, cannot get customer interest
- Pivot options: Change customer segment, adjust technical approach

**Decision Point 2: Build Regional Datacenter (Month 12)**

- Go if: >8 cables deployed, cloud costs >\$X/month, 1-3s latency required
- No-go if: <8 cables, cloud costs manageable, customers accept 5-30s latency
- Alternative: Colocate or continue cloud-only

**Decision Point 3: Series B / International Expansion (Month 18)**

- Go if: \$X ARR, Y cables, Z% gross margin, clear path to profitability
- No-go if: Customer acquisition slower than projected, unit economics poor
- Pivot options: Focus on single geography, change pricing model

### 6.3 Risk Triggers & Mitigation

**Technical Risks:**

- Trigger: Detection accuracy <X% after Y dataset validations
  - Mitigation: Increase R&D budget, hire expert advisor, consider lossless compression
- Trigger: Compression loses critical information for use case Z
  - Mitigation: Deploy GPU at edge for affected customers, adjust pricing

**Cost Risks:**

- Trigger: Cloud costs >\$X/month and growing unsustainably
  - Mitigation: Accelerate regional datacenter build, negotiate cloud discounts
- Trigger: Gross margin <X% by Month Y
  - Mitigation: Increase prices, reduce edge costs, optimize cloud usage

**Team Risks:**

- Trigger: Cannot hire X engineers by Month Y
  - Mitigation: Increase salaries, use contractors, reduce scope
- Trigger: Key engineer departs (CTO, Head of ML)
  - Mitigation: Hire backup, cross-train team, retain with equity

**Customer Risks:**

- Trigger: <X lighthouse customers signed by Month Y
  - Mitigation: Pivot customer segment, adjust pricing, enhance product
- Trigger: Customer churn >X% per month
  - Mitigation: Improve product quality, increase support, adjust pricing

---

## Section 7: Action Items & Owners

### Immediate Actions (Next 30 Days)

| Action Item                                           | Owner     | Deadline | Success Criteria              |
| ----------------------------------------------------- | --------- | -------- | ----------------------------- |
| Answer all Section 1 questions (Technical Validation) | CTO       | [DATE]   | Documented in PRD             |
| Answer all Section 2 questions (Architectural Scale)  | CTO + CFO | [DATE]   | Roadmap with decision points  |
| Answer all Section 4 questions (Team & Resourcing)    | CEO + CTO | [DATE]   | Hiring plan & budget          |
| Answer all Section 5 questions (Cost Metrics)         | CFO       | [DATE]   | Cost model & targets          |
| Define Phase 1 milestones with dates and budgets      | CEO       | [DATE]   | Project plan with Gantt chart |

### Short-Term Actions (Next 90 Days)

| Action Item                                             | Owner | Deadline | Success Criteria      |
| ------------------------------------------------------- | ----- | -------- | --------------------- |
| Complete technical validation (Section 1.1)             | CTO   | [DATE]   | Validation report     |
| Secure lighthouse customers (Section 1.2)               | CEO   | [DATE]   | 2+ LOIs signed        |
| Choose cloud provider & negotiate credits (Section 2.3) | CTO   | [DATE]   | \$Xk credits secured  |
| Hire first 5 engineers (Section 4)                      | CEO   | [DATE]   | 5 engineers onboarded |
| Implement cost dashboard (Section 5.2)                  | CFO   | [DATE]   | Dashboard live        |

### Long-Term Actions (Next 6-12 Months)

| Action Item                                    | Owner | Deadline   | Success Criteria       |
| ---------------------------------------------- | ----- | ---------- | ---------------------- |
| Make architecture decision (Option B or C)     | CTO   | Month 6-12 | Documented decision    |
| Build or lease regional datacenter (if needed) | CTO   | Month 12   | Datacenter operational |
| Scale team to X engineers                      | CEO   | Month 12   | X engineers productive |
| Achieve \$Xk MRR                               | CEO   | Month 12   | Revenue milestone      |
| Deploy X cables                                | CTO   | Month 12   | X cables operational   |

---

## Appendix: Decision Templates

### Template 1: Technical Validation Checklist

```markdown
## Validation: [Vessel Detection Accuracy at ε=0.1 Compression]

**Hypothesis**: Compression with ε=0.1 preserves >97% of vessel information

**Test Plan**:

1. Dataset: X hours of DAS data with Y vessel passages
2. Method: Compare detection accuracy (raw vs compressed)
3. Success criteria: <3% accuracy degradation

**Resources**:

- Personnel: 2 engineers × 4 weeks
- Compute: \$X for cloud GPU hours
- Data: Y TB of test data

**Timeline**: Complete by [DATE]

**Results**: [TO BE FILLED]

**Decision**: Go / No-Go / Adjust parameters
```

### Template 2: Architecture Decision Record

```markdown
## ADR-XXX: [Choose CPU + Regional Datacenter (Option B)]

**Context**: Need to decide between Option A (GPU Edge), Option B (Regional DC), Option C (Cloud)

**Decision**: [OPTION B - CPU + Regional Datacenter]

**Rationale**:

- Customer latency requirement: 1-3 seconds acceptable for X% of customers
- Cost: $460k per cable at 20 cables vs $500k for Option A
- Scalability: Centralized GPU allows algorithm updates
- Risk: Information theory proves compression preserves 97% vessel info

**Consequences**:

- Positive: Cost savings, flexibility, scalability
- Negative: Slightly higher latency than Option A
- Mitigation: Offer Option A for premium customers if needed

**Validation**: Deploy Option C first for pilots, migrate to Option B at 10 cables

**Date**: [DATE]
**Owner**: CTO
**Reviewers**: CEO, CFO, Board
```

### Template 3: Cost Model Spreadsheet Structure

```
Tab 1: Unit Economics
- Cost per cable (edge, datacenter, cloud)
- Revenue per cable (by customer type)
- Gross margin

Tab 2: Phase Planning
- Phase 1: X cables, $Y cost, $Z revenue
- Phase 2: X cables, $Y cost, $Z revenue
- Phase 3: X cables, $Y cost, $Z revenue

Tab 3: Cloud Costs
- Compute (GPU, CPU by service)
- Storage (hot, warm, cold)
- Network (ingress, egress)
- By month, by cable

Tab 4: Team Costs
- By role, by phase
- Salaries, benefits, contractors
- Total team cost by month

Tab 5: Vendor Comparison
- GCP vs AWS vs Azure
- List prices, negotiated prices, volume discounts
- 1-year, 3-year, 5-year TCO
```

---

## Summary: Key Decisions Needed

This document identifies **87 critical questions** across 7 areas that need answers to set milestones:

1. **Technical Validation (20 questions)**: What do we need to prove and by when?
2. **Architectural Scale (18 questions)**: When do we build/scale infrastructure?
3. **Partner Engagement (16 questions)**: Who do we partner with and when?
4. **Team & Resourcing (15 questions)**: How many people, what roles, when hired?
5. **Cost Metrics (10 questions)**: What do we track and what are our targets?
6. **Multi-Vendor Comparison (8 questions)**: How do we compare and negotiate?
7. **Success Criteria (TBD)**: What are our go/no-go triggers?

**Next Step**: Schedule working sessions to answer these questions and build the detailed roadmap with milestones, dates, budgets, and owners.

**Estimated Time**: 3-5 full-day working sessions with CEO, CTO, CFO + key hires

**Output**:

- Detailed project plan with milestones
- Budget model with cost targets
- Hiring plan with timeline
- Partner engagement roadmap
- Cost dashboard specifications
- Go/no-go decision criteria

## **Timeline**: Complete all answers within 30 days to enable Series A pitch and execution

layout: default
title: "Internal Decision Questions for Milestone Planning"
description: "Strategic questions to answer internally for defining milestones in technical validation, architectural scale, and partner engagement with focus on team resourcing and cost metrics."

---

# Internal Decision Questions for Milestone Planning

## Purpose

This document contains critical questions **you need to answer internally** to set concrete milestones and targets for:

1. **Technical Validation** - What do we need to prove technically?
2. **Architectural Scale** - When and how do we scale infrastructure?
3. **Partner Engagement** - Who do we engage and when?

Special focus on:

- Team size and resourcing for multi-cloud services design
- Dashboards/metrics for platform costs
- Multi-vendor comparisons

---

## Section 1: Technical Validation Milestones

### 1.1 Compression Fidelity Validation

**Questions to Answer:**

1. **What specific vessel detection accuracy degradation is acceptable?**

   - Is 97% preservation of vessel information (2.9/3.0 bits) sufficient for our primary use cases?
   - At what accuracy threshold would customers reject the product? (99.9%, 99.5%, 99%, 95%?)
   - Do different customer segments have different accuracy requirements?

2. **What compression error thresholds need validation?**

   - Current plan: ε=0.1 (low loss), ε=0.5 (high loss)
   - Do we need to validate: ε=0.05, 0.1, 0.2, 0.5, 1.0?
   - How many real-world datasets are needed to validate each threshold?
   - Timeline: How long to acquire and validate each dataset?

3. **What vessel types/scenarios MUST be validated before launch?**
   - Large cargo ships (>10k tons): Required for MVP?
   - Medium vessels (1-10k tons): Required for MVP?
   - Small vessels (<1k tons): Required for MVP?
   - Submarines: Required for MVP or Phase 2?
   - Overlapping vessels: Required validation?
   - Adverse weather/high sea state: Required validation?

**Milestone Definition Needed:**

- [ ] Define minimum dataset size for validation (X hours of data, Y vessel passages)
- [ ] Define acceptance criteria: "99.X% accuracy on Z vessel types with ε=W compression"
- [ ] Set timeline: Complete validation by [DATE]
- [ ] Budget: Allocate \$XXk for data acquisition and validation compute

### 1.2 Latency Requirements Validation

**Questions to Answer:**

1. **What latency is acceptable for each customer segment?**

   - Ports: <1s, <3s, <10s, or <30s acceptable?
   - Coast Guard: <1s, <3s, or <10s?
   - Environmental agencies: Minutes acceptable?
   - Research institutions: Hours acceptable?

2. **Can we validate latency acceptance with lighthouse customers before committing to architecture?**

   - Approach: Deploy Option C (cloud, 5-30s latency) for pilots
   - Get customer feedback on whether they'd pay MORE for <3s (Option B) or <1s (Option A)
   - Milestone: "3 lighthouse customers confirm latency requirements by [DATE]"

3. **What's the network latency budget breakdown?**
   - Edge to regional datacenter: Target X ms
   - Regional datacenter processing: Target Y ms
   - Datacenter to cloud: Target Z ms
   - End-to-end acceptable: <3000 ms total?
   - Milestone: "Network latency validated on 3 geographic routes by [DATE]"

**Milestone Definition Needed:**

- [ ] Complete customer interviews on latency requirements by [DATE]
- [ ] Document latency requirements per customer segment in product spec
- [ ] Validate network paths achieve <Xms edge-to-datacenter on Y routes by [DATE]

### 1.3 Multi-Cable Correlation Validation

**Questions to Answer:**

1. **At what scale do we need multi-cable correlation working?**

   - MVP (5 cables): Single-cable detection sufficient?
   - Phase 2 (15 cables): Multi-cable correlation required?
   - Phase 3 (30 cables): Full vessel tracking across network?

2. **What vessel tracking accuracy is required?**

   - Position estimation: Within X meters/kilometers?
   - Velocity estimation: Within Y knots?
   - Vessel ID consistency: Z% of time same vessel identified across cables?

3. **What's the time synchronization requirement?**
   - GPS-disciplined oscillators at each site: Required by MVP?
   - Time sync accuracy: <1ms, <10ms, <100ms?
   - Budget: \$Xk per site for time sync hardware

**Milestone Definition Needed:**

- [ ] Define multi-cable correlation requirements by Phase (1, 2, 3)
- [ ] Validate time synchronization approach on 2 cable sites by [DATE]
- [ ] Achieve X% vessel tracking accuracy across Y cables by [DATE]

---

## Section 2: Architectural Scale Milestones

### 2.1 Architecture Decision Timeline

**Critical Questions:**

1. **When do we COMMIT to Option B (CPU + Regional DC) vs Option C (CPU + Cloud)?**

   - Trigger: After X customer pilots?
   - Trigger: After Y cables deployed?
   - Trigger: After validating Z technical metrics?
   - Timeline: Decide by [DATE] to allow for datacenter buildout

2. **What's the decision criteria for building first regional datacenter?**

   - Number of cables: 8, 10, or 15 cables?
   - Geographic density: X cables within Y km radius?
   - Customer contracts: \$Z ARR committed?
   - Timeline: Decision point at Month X, operational by Month Y

3. **Do we build, colocate, or lease datacenter infrastructure?**
   - Build: \$2M capex, 6-month timeline, full control
   - Colocate: $500k setup + $200k/year, 3-month timeline, less control
   - Lease GPU cloud: \$XXk/month, immediate, operational flexibility
   - Decision needed by: [DATE]

**Milestone Definition Needed:**

- [ ] Set decision trigger: "Choose Option B vs C by [DATE] or [X cables] or [$Y ARR]"
- [ ] Evaluate 3 datacenter locations (US/EU/APAC) by [DATE]
- [ ] Complete build vs colocate vs lease analysis by [DATE]
- [ ] Budget: Reserve \$2M for potential datacenter if triggered

### 2.2 Edge Infrastructure Scaling

**Questions to Answer:**

1. **What's our edge deployment capacity?**

   - Current capability: X cables per quarter
   - Target capability: Y cables per quarter by Q[X]
   - Bottleneck: Hardware procurement, installation teams, or site negotiations?
   - Resource needed: Z installation teams, W site engineers

2. **Do we standardize on single edge hardware config or multiple?**

   - Single config: \$350k CPU-only for all sites (simpler ops)
   - Multi-tier: $500k GPU for Tier 1, $350k CPU for Tier 2 (complex ops)
   - Decision criteria: Customer requirements, or operational simplicity?

3. **What's our edge hardware refresh strategy?**
   - Lifetime: 5 years, 7 years, or 10 years?
   - Upgrade path: Replace CPUs, add GPUs, or swap entire system?
   - Budget: \$XXk per site per year for hardware refresh

**Milestone Definition Needed:**

- [ ] Define standard edge hardware BOM by [DATE]
- [ ] Negotiate hardware agreements with X vendors by [DATE]
- [ ] Build installation team capacity to Y cables/quarter by Q[X]
- [ ] Establish installation playbook and deployment timeline (<30 days per site)

### 2.3 Cloud/Multi-Cloud Strategy

**Questions to Answer:**

1. **Single cloud or multi-cloud from Day 1?**

   - Single (GCP/AWS/Azure): Faster MVP, vendor lock-in risk
   - Multi-cloud: Slower development, better negotiating position
   - Hybrid: Core on one cloud, DR/overflow on second?

2. **What cloud services are we committed to vs abstracted?**

   - Kubernetes: Portable across clouds (use)
   - Managed databases: Cloud-specific (abstract with ORM or accept lock-in?)
   - Object storage: Portable (S3 API standard)
   - ML platforms: Cloud-specific (Vertex AI vs SageMaker vs Azure ML - commit or abstract?)

3. **What's our cloud cost budget by phase?**

   - Phase 1 (3-5 cables): \$Xk/month acceptable?
   - Phase 2 (15 cables): \$Yk/month acceptable?
   - Phase 3 (30 cables): \$Zk/month acceptable?
   - Trigger: Build regional datacenter if cloud costs exceed \$X/month?

4. **What cloud regions are required?**
   - US: us-west-2 (Oregon), us-east-1 (Virginia)?
   - EU: eu-central-1 (Frankfurt)?
   - APAC: asia-northeast-1 (Tokyo)?
   - Latency requirement: <50ms edge-to-region for X% of sites?

**Milestone Definition Needed:**

- [ ] Choose primary cloud provider by [DATE](GCP/AWS/Azure)
- [ ] Complete multi-cloud feasibility study by [DATE]
- [ ] Negotiate cloud credits/discounts: Target \$Xk credits by [DATE]
- [ ] Define cloud cost budget by phase and set up cost monitoring
- [ ] Set trigger: "Move to regional datacenter if cloud compute >\$X/month for Y months"

---

## Section 3: Partner Engagement Strategy

### 3.1 Cable Operator Partnerships

**Questions to Answer:**

1. **What's our cable operator engagement priority?**

   - Rank by: Geographic coverage, customer access, or technical capability?
   - Top 3 targets: SubCom, Alcatel, NEC, or others?
   - Engagement model: Revenue share (20%?), licensing fee, or joint venture?

2. **What do we need FROM cable operators?**

   - Access to cable landing stations (site space, power, network)
   - Introductions to cable customers (ports, telecom, government)
   - Technical support (fiber specs, interrogator integration)
   - Co-marketing (joint go-to-market)

3. **What milestones trigger cable operator engagement?**
   - Trigger 1: After technical validation complete (Month X)?
   - Trigger 2: After first lighthouse customer signed?
   - Trigger 3: After Series A funding secured?

**Milestone Definition Needed:**

- [ ] Rank top 5 cable operators by priority by [DATE]
- [ ] Prepare partnership proposal (revenue share %, term sheet) by [DATE]
- [ ] Secure first cable operator MOU/partnership by [DATE]
- [ ] Target: X cable operator partnerships by end of Year 1

### 3.2 Cloud Provider Partnerships

**Questions to Answer:**

1. **What's our ask from cloud providers?**

   - Cloud credits: $Xk in startup credits (typical: $100k-\$500k)
   - Technical support: Dedicated solutions architect?
   - Co-selling: Introduction to maritime/government customers?
   - Technology access: Early access to GPUs, TPUs, edge compute?

2. **Which cloud provider offers best strategic value?**

   - GCP: Strong ML/AI, submarine cable operator, Google engineer connection
   - AWS: Dominant market share, GovCloud for military customers
   - Azure: Government relationships, hybrid cloud capabilities
   - Scoring criteria: Credits, technical fit, customer access, strategic alignment

3. **What milestones unlock cloud partnership benefits?**
   - Startup credits: Application process, requires [X documentation]
   - Solutions architect: Requires \$Xk/month spend commitment?
   - Co-selling: Requires customer case study or [Y] validation?

**Milestone Definition Needed:**

- [ ] Apply for GCP/AWS/Azure startup programs by [DATE]
- [ ] Secure \$Xk cloud credits commitment by [DATE]
- [ ] Meet with cloud provider enterprise sales by [DATE]
- [ ] Negotiate volume discounts (target: X% off list price at Y scale) by [DATE]

### 3.3 System Integrator Partnerships

**Questions to Answer:**

1. **When do we need system integrator (SI) partnerships?**

   - For government/military sales: Required immediately or Phase 2?
   - For large port authorities: Required immediately or can sell direct?
   - For international expansion: Required for which geographies?

2. **Which SIs are priority partners?**

   - Defense: Lockheed Martin, Raytheon, Northrop Grumman, Thales
   - Maritime: Kongsberg, Wartsila, others?
   - IT/Cloud: Accenture, Deloitte, others?
   - Selection criteria: Customer access, technical capability, partnership terms

3. **What partnership model?**
   - Reseller: SI sells our product (X% margin)
   - Referral: SI introduces customers (Y% referral fee)
   - Co-development: SI integrates our product into their solutions (revenue share)
   - OEM: SI white-labels our technology (licensing model)

**Milestone Definition Needed:**

- [ ] Identify top 3 SI partners per segment (defense, maritime, IT) by [DATE]
- [ ] Prepare SI partnership proposal and pricing by [DATE]
- [ ] Sign first SI partnership agreement by [DATE]
- [ ] Target: X SI partnerships by end of Year 1

### 3.4 Technology/Research Partnerships

**Questions to Answer:**

1. **Do we need academic/research partnerships?**

   - For: Algorithm validation, publications, credibility
   - Against: Slower, IP concerns, resource intensive
   - Candidates: MIT, Stanford, NOAA, Naval Postgraduate School?

2. **What do we need from research partners?**

   - Access to datasets for ML training
   - Algorithm validation and peer review
   - Student interns/recruiting pipeline
   - Publications for credibility

3. **What milestones justify research partnerships?**
   - Phase 1: Focus on product, no bandwidth for research?
   - Phase 2: Once product proven, invest in advanced R&D?
   - Continuous: Academic advisory board from Day 1?

**Milestone Definition Needed:**

- [ ] Decide on research partnership strategy (yes/no/later) by [DATE]
- [ ] If yes: Identify top 3 research partners and engagement model by [DATE]
- [ ] Establish academic advisory board (X professors) by [DATE]

---

## Section 4: Team Size & Resourcing

### 4.1 Multi-Cloud Services Design Team

**Critical Questions:**

1. **What team size is required for multi-cloud platform development?**

   - Platform architecture: X cloud architects
   - DevOps/SRE: Y engineers for infrastructure-as-code, CI/CD
   - Security: Z engineers for multi-cloud security, compliance
   - Total team: X + Y + Z = ? engineers

2. **What skills are required for multi-cloud expertise?**

   - Must have: Kubernetes, Terraform, Docker, CI/CD
   - Cloud-specific: GCP/AWS/Azure certifications
   - Specialized: Multi-cloud networking, security, cost optimization
   - Seniority: Senior (5+ years) vs mid-level (2-5 years) ratio?

3. **Build vs hire vs outsource for multi-cloud team?**

   - Build internal team: X FTEs at $Y salary = $Z annual cost
   - Hire consultancy: $X per hour, Y hours = $Z project cost
   - Hybrid: Core internal team + consultants for peaks
   - Decision criteria: Time to market, cost, long-term capability

4. **What's the team ramp schedule?**
   - Month 0-3: X engineers (core platform)
   - Month 3-6: Y engineers (add ML platform)
   - Month 6-12: Z engineers (scale operations)
   - Year 2: W engineers (multi-region expansion)

**Milestone Definition Needed:**

- [ ] Define multi-cloud platform team structure by [DATE]
- [ ] Budget: Allocate $Xk for Year 1 salaries ($150k-\$200k per engineer)
- [ ] Create job descriptions and begin recruiting by [DATE]
- [ ] Target: Hire X engineers by [QUARTER], Y engineers by [QUARTER]
- [ ] Decide build vs hire vs outsource strategy by [DATE]

### 4.2 Edge/Hardware Team

**Questions to Answer:**

1. **What team is required for edge infrastructure at scale?**

   - Hardware design/procurement: X engineers
   - Installation/deployment: Y field engineers
   - Support/maintenance: Z remote support engineers
   - Total team: X + Y + Z = ? engineers
   - Scaling: Team size at 5 cables, 15 cables, 30 cables?

2. **How many installation teams do we need?**

   - Installation time per site: X days
   - Target deployment rate: Y cables per quarter
   - Required teams: Z teams (assume 1 team = 2-3 engineers)
   - Team cost: \$Xk per team per year

3. **Build internal installation teams vs contractors?**
   - Internal: Higher quality, slower ramp, higher fixed cost
   - Contractors: Faster ramp, variable cost, less control
   - Hybrid: Internal project managers + contractor labor?

**Milestone Definition Needed:**

- [ ] Define edge team structure and size by [DATE]
- [ ] Budget: $Xk for edge team Year 1 (Y engineers at $Z salary)
- [ ] Recruit/train first installation team by [DATE]
- [ ] Complete X successful installations as validation by [DATE]
- [ ] Scale to Y installation teams by [QUARTER] to support Z cables/quarter

### 4.3 Signal Processing & ML Team

**Questions to Answer:**

1. **What team size for core algorithms?**

   - Signal processing (FFT, compression): X PhDs/experts
   - ML/classification: Y ML engineers
   - Computer vision (if applicable): Z engineers
   - Total: X + Y + Z = ? engineers
   - Timeline: Build team by Month X to support launch

2. **What seniority/expertise is required?**

   - Senior/Staff level (PhD or 10+ years): X engineers
   - Mid-level (3-5 years): Y engineers
   - Junior (0-2 years): Z engineers
   - Specific expertise: Acoustic signal processing, marine acoustic classification

3. **External advisors vs internal team?**
   - Core algorithms: Must be internal (IP ownership)
   - Domain expertise: Advisors acceptable (marine acoustics, oceanography)
   - Consulting model: $X per hour for Y hours = $Z budget

**Milestone Definition Needed:**

- [ ] Define signal processing/ML team structure by [DATE]
- [ ] Budget: $Xk for Year 1 ($180k-\$250k per senior engineer)
- [ ] Recruit Head of Signal Processing/ML by [DATE]
- [ ] Hire X engineers by [QUARTER], Y engineers by [QUARTER]
- [ ] Establish advisor network (X advisors, Y domains) by [DATE]

### 4.4 Data Engineering Team

**Questions to Answer:**

1. **What data team size is required?**

   - Streaming data engineering: X engineers (Kafka, Kinesis, real-time)
   - Batch data engineering: Y engineers (Spark, data lake, ETL)
   - Data infrastructure: Z engineers (databases, storage, pipelines)
   - Total: X + Y + Z = ? engineers

2. **What's the data team ramp?**

   - Phase 1 (single cable): X engineers sufficient
   - Phase 2 (10 cables): Y engineers required
   - Phase 3 (30 cables): Z engineers required
   - Scaling trigger: Add engineer per X cables?

3. **What data roles are critical vs nice-to-have?**
   - Critical (must have for MVP): Data pipeline engineer, infrastructure engineer
   - Important (Phase 2): Data scientist, analytics engineer
   - Nice-to-have (Phase 3): ML platform engineer, data governance

**Milestone Definition Needed:**

- [ ] Define data team structure by [DATE]
- [ ] Budget: $Xk for Year 1 ($150k-\$180k per engineer)
- [ ] Hire first data engineers (X engineers) by [DATE]
- [ ] Build MVP data pipeline by [DATE]
- [ ] Scale team to Y engineers by [QUARTER]

### 4.5 Overall Team Budget

**Questions to Answer:**

1. **What's the total engineering team size and cost?**

   - Year 1: X engineers at average $Y salary = $Z total
   - Year 2: X engineers at average $Y salary = $Z total
   - Year 3: X engineers at average $Y salary = $Z total

2. **What's the engineering vs non-engineering split?**

   - Engineering (product, platform, ML): X% of team
   - Sales & Marketing: Y% of team
   - Operations: Z% of team
   - Executive & Admin: W% of team

3. **Does our Series A funding support this team?**
   - Series A: \$10M total
   - Engineering budget (30%): \$3M for 18 months
   - Salaries: $3M / 18 months = $167k/month = ~15-20 engineers average
   - Is this sufficient for: Multi-cloud (3), edge (4), ML (4), data (3), product (3) = 17 engineers?

**Milestone Definition Needed:**

- [ ] Complete detailed team budget model by [DATE]
- [ ] Validate team size fits Series A budget by [DATE]
- [ ] Set team size milestones: X engineers by Month 6, Y by Month 12, Z by Month 18
- [ ] Define hiring priority: Role 1, Role 2, Role 3, ... Role N

---

## Section 5: Cost Metrics & Dashboards

### 5.1 Platform Cost Metrics

**Critical Questions:**

1. **What cost metrics do we track?**

   - Cost per cable per month: Target \$X
   - Cost per TB processed: Target \$Y
   - Cost per vessel detection: Target \$Z
   - Cost per customer per month: Target \$W
   - Gross margin per cable: Target X%

2. **What's the cost breakdown structure?**

   ```
   Total Cost per Cable
   ├── Edge Infrastructure
   │   ├── Hardware (amortized): $X/month
   │   ├── Power & Cooling: $Y/month
   │   ├── Bandwidth: $Z/month
   │   └── Maintenance: $W/month
   ├── Cloud/Datacenter Compute
   │   ├── FFT Processing: $X/month
   │   ├── ML Inference: $Y/month
   │   ├── Data Storage: $Z/month
   │   └── Network egress: $W/month
   ├── Personnel (allocated)
   │   ├── Engineering (amortized): $X/month
   │   ├── Support: $Y/month
   │   └── Operations: $Z/month
   └── Total: $XX,XXX/month
   ```

3. **What are our cost targets by phase?**

   - Phase 1 (5 cables): Total cost $X/month, cost per cable $Y
   - Phase 2 (15 cables): Total cost $X/month, cost per cable $Y (20% reduction)
   - Phase 3 (30 cables): Total cost $X/month, cost per cable $Y (40% reduction)
   - Economies of scale: X% cost reduction per doubling of cables

4. **What's our gross margin target?**
   - Year 1: X% (acceptable due to fixed cost scaling)
   - Year 2: Y% (target 60%?)
   - Year 3: Z% (target 70%?)
   - Competitive benchmark: What margin do Spire Maritime, exactEarth have?

**Milestone Definition Needed:**

- [ ] Define cost metrics and targets by [DATE]
- [ ] Build cost tracking spreadsheet/dashboard by [DATE]
- [ ] Set cost reduction targets: X% per quarter, Y% per year
- [ ] Achieve cost per cable <\$X by [QUARTER]
- [ ] Achieve gross margin >X% by [QUARTER]

### 5.2 Cost Dashboard Requirements

**Questions to Answer:**

1. **What cost dashboards do we need?**

   - Executive dashboard: Total cost, cost per cable, gross margin (monthly)
   - Engineering dashboard: Cloud costs by service, compute utilization (daily)
   - Operations dashboard: Edge costs, bandwidth usage, outages (real-time)
   - Finance dashboard: P&L by customer segment, unit economics (monthly)

2. **What drill-down capabilities are required?**

   - Total cost → By cable → By infrastructure component → By cloud service
   - By time: Month, week, day, hour
   - By geography: US, EU, APAC
   - By customer type: Port, naval, environmental

3. **What alerting do we need on cost metrics?**

   - Alert: Cloud costs exceed \$X/day for Y consecutive days
   - Alert: Cost per cable increases >X% month-over-month
   - Alert: Gross margin falls below X%
   - Alert: Specific service costs spike >X% from baseline

4. **What tools do we use for cost tracking?**
   - Cloud-native: GCP Cost Management, AWS Cost Explorer, Azure Cost Management
   - Third-party: Kubecost, CloudHealth, Datadog
   - Custom: Build internal dashboard (Grafana, Tableau, etc.)
   - Decision criteria: Integration, granularity, cost of tool itself

**Milestone Definition Needed:**

- [ ] Define cost dashboard requirements by [DATE]
- [ ] Choose cost tracking tools by [DATE]
- [ ] Implement MVP cost dashboard by [DATE]
- [ ] Train team on cost monitoring by [DATE]
- [ ] Establish weekly cost review meeting by [DATE]

### 5.3 Multi-Vendor Cost Comparison

**Questions to Answer:**

1. **What vendors do we need to compare?**

   - Cloud compute: GCP vs AWS vs Azure (GPU costs)
   - Cloud storage: GCP Cloud Storage vs AWS S3 vs Azure Blob
   - Managed services: GKE vs EKS vs AKS (Kubernetes)
   - Networking: Cloud interconnect vs dedicated fiber vs SD-WAN
   - Edge hardware: NVIDIA vs AMD GPUs, Intel vs AMD CPUs

2. **What's our cost comparison methodology?**

   - Baseline workload definition: X TB/day processing, Y GPU hours, Z TB storage
   - Vendor quotes: List price, negotiated discount, volume commitments
   - TCO analysis: 1 year, 3 years, 5 years
   - Include: Setup costs, migration costs, operational complexity

3. **When do we trigger multi-vendor RFP?**

   - Trigger 1: At \$X/month spend (negotiate better rates)
   - Trigger 2: Annual contract renewal
   - Trigger 3: Before committing to regional datacenter
   - Timeline: Run RFP process every X months

4. **What's our multi-cloud strategy for cost optimization?**
   - Single cloud with annual negotiations (simpler)
   - Multi-cloud for cost arbitrage (more complex, operational overhead)
   - Hybrid: Primary cloud + backup for DR and price negotiation leverage
   - Decision: Single vs multi-cloud by [DATE]

**Milestone Definition Needed:**

- [ ] Define vendor comparison framework by [DATE]
- [ ] Run initial RFP for cloud providers by [DATE]
- [ ] Negotiate X% discount off list prices by [DATE]
- [ ] Establish annual RFP process for major vendors
- [ ] Document vendor switching costs (prevents lock-in) by [DATE]

### 5.4 Cost Optimization Strategy

**Questions to Answer:**

1. **What are our top cost optimization opportunities?**

   - Compute: Spot instances (AWS/GCP/Azure) save X%, acceptable for batch jobs?
   - Storage: Tiered storage (hot/warm/cold) saves Y%, retention policy defined?
   - Networking: Reduce egress costs by Z%, use private links/colocation?
   - Compression: Higher compression ratios save W% storage, acceptable quality loss?

2. **What cost optimization timeline?**

   - Phase 1: Accept higher costs for speed (move fast)
   - Phase 2: Optimize obvious inefficiencies (low-hanging fruit)
   - Phase 3: Deep optimization for profitability (after product-market fit)
   - Milestones: Achieve X% cost reduction in Phase 2, Y% in Phase 3

3. **What's the trade-off between cost and complexity?**

   - Example: Multi-cloud saves X% but adds Y engineering overhead
   - Example: Spot instances save X% but add Z reliability complexity
   - Decision framework: Optimize if savings > \$X/month OR >Y% improvement

4. **What cost controls do we put in place?**
   - Budget limits: Cloud spending capped at \$X/month, alerts at 80%
   - Approval process: Spending >\$Y requires approval
   - Resource tagging: All cloud resources tagged (cable_id, environment, team)
   - Regular reviews: Weekly cost review, monthly optimization sprint

**Milestone Definition Needed:**

- [ ] Identify top 5 cost optimization opportunities by [DATE]
- [ ] Implement cost controls (budgets, approvals, tagging) by [DATE]
- [ ] Achieve X% cost reduction through optimization by [QUARTER]
- [ ] Establish cost optimization culture (monthly review, team targets) by [DATE]

---

## Section 6: Success Criteria & Checkpoints

### 6.1 Technical Validation Success Criteria

**Define by Phase:**

**Phase 1 (Months 0-6): Proof of Concept**

- [ ] Compression validation: X% vessel information preserved at ε=0.1
- [ ] Detection accuracy: Y% on Z vessel types
- [ ] Latency: <W seconds end-to-end
- [ ] System uptime: >X% over Y day period

**Phase 2 (Months 6-12): Pilot Deployment**

- [ ] Multi-cable correlation: X% tracking accuracy across Y cables
- [ ] Customer validation: Z lighthouse customers confirm value
- [ ] Scalability: Process data from X cables simultaneously
- [ ] Cost: Achieve <\$Y cost per cable per month

**Phase 3 (Months 12-18): Scale & Refine**

- [ ] Architecture decision: Commit to Option B or C based on validation
- [ ] Team scale: X engineers hired and productive
- [ ] Customer scale: Y paid customers, \$Z ARR
- [ ] Infrastructure scale: W cables deployed and operational

### 6.2 Go/No-Go Decision Points

**Decision Point 1: Proceed to Series A (Month 3)**

- Go if: Technical validation complete, 2+ LOIs from customers
- No-go if: Detection accuracy <X%, cannot get customer interest
- Pivot options: Change customer segment, adjust technical approach

**Decision Point 2: Build Regional Datacenter (Month 12)**

- Go if: >8 cables deployed, cloud costs >\$X/month, 1-3s latency required
- No-go if: <8 cables, cloud costs manageable, customers accept 5-30s latency
- Alternative: Colocate or continue cloud-only

**Decision Point 3: Series B / International Expansion (Month 18)**

- Go if: \$X ARR, Y cables, Z% gross margin, clear path to profitability
- No-go if: Customer acquisition slower than projected, unit economics poor
- Pivot options: Focus on single geography, change pricing model

### 6.3 Risk Triggers & Mitigation

**Technical Risks:**

- Trigger: Detection accuracy <X% after Y dataset validations
  - Mitigation: Increase R&D budget, hire expert advisor, consider lossless compression
- Trigger: Compression loses critical information for use case Z
  - Mitigation: Deploy GPU at edge for affected customers, adjust pricing

**Cost Risks:**

- Trigger: Cloud costs >\$X/month and growing unsustainably
  - Mitigation: Accelerate regional datacenter build, negotiate cloud discounts
- Trigger: Gross margin <X% by Month Y
  - Mitigation: Increase prices, reduce edge costs, optimize cloud usage

**Team Risks:**

- Trigger: Cannot hire X engineers by Month Y
  - Mitigation: Increase salaries, use contractors, reduce scope
- Trigger: Key engineer departs (CTO, Head of ML)
  - Mitigation: Hire backup, cross-train team, retain with equity

**Customer Risks:**

- Trigger: <X lighthouse customers signed by Month Y
  - Mitigation: Pivot customer segment, adjust pricing, enhance product
- Trigger: Customer churn >X% per month
  - Mitigation: Improve product quality, increase support, adjust pricing

---

## Section 7: Action Items & Owners

### Immediate Actions (Next 30 Days)

| Action Item                                           | Owner     | Deadline | Success Criteria              |
| ----------------------------------------------------- | --------- | -------- | ----------------------------- |
| Answer all Section 1 questions (Technical Validation) | CTO       | [DATE]   | Documented in PRD             |
| Answer all Section 2 questions (Architectural Scale)  | CTO + CFO | [DATE]   | Roadmap with decision points  |
| Answer all Section 4 questions (Team & Resourcing)    | CEO + CTO | [DATE]   | Hiring plan & budget          |
| Answer all Section 5 questions (Cost Metrics)         | CFO       | [DATE]   | Cost model & targets          |
| Define Phase 1 milestones with dates and budgets      | CEO       | [DATE]   | Project plan with Gantt chart |

### Short-Term Actions (Next 90 Days)

| Action Item                                             | Owner | Deadline | Success Criteria      |
| ------------------------------------------------------- | ----- | -------- | --------------------- |
| Complete technical validation (Section 1.1)             | CTO   | [DATE]   | Validation report     |
| Secure lighthouse customers (Section 1.2)               | CEO   | [DATE]   | 2+ LOIs signed        |
| Choose cloud provider & negotiate credits (Section 2.3) | CTO   | [DATE]   | \$Xk credits secured  |
| Hire first 5 engineers (Section 4)                      | CEO   | [DATE]   | 5 engineers onboarded |
| Implement cost dashboard (Section 5.2)                  | CFO   | [DATE]   | Dashboard live        |

### Long-Term Actions (Next 6-12 Months)

| Action Item                                    | Owner | Deadline   | Success Criteria       |
| ---------------------------------------------- | ----- | ---------- | ---------------------- |
| Make architecture decision (Option B or C)     | CTO   | Month 6-12 | Documented decision    |
| Build or lease regional datacenter (if needed) | CTO   | Month 12   | Datacenter operational |
| Scale team to X engineers                      | CEO   | Month 12   | X engineers productive |
| Achieve \$Xk MRR                               | CEO   | Month 12   | Revenue milestone      |
| Deploy X cables                                | CTO   | Month 12   | X cables operational   |

---

## Appendix: Decision Templates

### Template 1: Technical Validation Checklist

```markdown
## Validation: [Vessel Detection Accuracy at ε=0.1 Compression]

**Hypothesis**: Compression with ε=0.1 preserves >97% of vessel information

**Test Plan**:

1. Dataset: X hours of DAS data with Y vessel passages
2. Method: Compare detection accuracy (raw vs compressed)
3. Success criteria: <3% accuracy degradation

**Resources**:

- Personnel: 2 engineers × 4 weeks
- Compute: \$X for cloud GPU hours
- Data: Y TB of test data

**Timeline**: Complete by [DATE]

**Results**: [TO BE FILLED]

**Decision**: Go / No-Go / Adjust parameters
```

### Template 2: Architecture Decision Record

```markdown
## ADR-XXX: [Choose CPU + Regional Datacenter (Option B)]

**Context**: Need to decide between Option A (GPU Edge), Option B (Regional DC), Option C (Cloud)

**Decision**: [OPTION B - CPU + Regional Datacenter]

**Rationale**:

- Customer latency requirement: 1-3 seconds acceptable for X% of customers
- Cost: $460k per cable at 20 cables vs $500k for Option A
- Scalability: Centralized GPU allows algorithm updates
- Risk: Information theory proves compression preserves 97% vessel info

**Consequences**:

- Positive: Cost savings, flexibility, scalability
- Negative: Slightly higher latency than Option A
- Mitigation: Offer Option A for premium customers if needed

**Validation**: Deploy Option C first for pilots, migrate to Option B at 10 cables

**Date**: [DATE]
**Owner**: CTO
**Reviewers**: CEO, CFO, Board
```

### Template 3: Cost Model Spreadsheet Structure

```
Tab 1: Unit Economics
- Cost per cable (edge, datacenter, cloud)
- Revenue per cable (by customer type)
- Gross margin

Tab 2: Phase Planning
- Phase 1: X cables, $Y cost, $Z revenue
- Phase 2: X cables, $Y cost, $Z revenue
- Phase 3: X cables, $Y cost, $Z revenue

Tab 3: Cloud Costs
- Compute (GPU, CPU by service)
- Storage (hot, warm, cold)
- Network (ingress, egress)
- By month, by cable

Tab 4: Team Costs
- By role, by phase
- Salaries, benefits, contractors
- Total team cost by month

Tab 5: Vendor Comparison
- GCP vs AWS vs Azure
- List prices, negotiated prices, volume discounts
- 1-year, 3-year, 5-year TCO
```

---

## Summary: Key Decisions Needed

This document identifies **87 critical questions** across 7 areas that need answers to set milestones:

1. **Technical Validation (20 questions)**: What do we need to prove and by when?
2. **Architectural Scale (18 questions)**: When do we build/scale infrastructure?
3. **Partner Engagement (16 questions)**: Who do we partner with and when?
4. **Team & Resourcing (15 questions)**: How many people, what roles, when hired?
5. **Cost Metrics (10 questions)**: What do we track and what are our targets?
6. **Multi-Vendor Comparison (8 questions)**: How do we compare and negotiate?
7. **Success Criteria (TBD)**: What are our go/no-go triggers?

**Next Step**: Schedule working sessions to answer these questions and build the detailed roadmap with milestones, dates, budgets, and owners.

**Estimated Time**: 3-5 full-day working sessions with CEO, CTO, CFO + key hires

**Output**:

- Detailed project plan with milestones
- Budget model with cost targets
- Hiring plan with timeline
- Partner engagement roadmap
- Cost dashboard specifications
- Go/no-go decision criteria

**Timeline**: Complete all answers within 30 days to enable Series A pitch and execution
