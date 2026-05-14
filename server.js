require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const NodeCache = require('node-cache');
const PDFDocument = require('pdfkit');
const PptxGenJS = require('pptxgenjs');

const app = express();
const cache = new NodeCache({ stdTTL: 3600 }); // 1hr cache

app.use(cors({ origin: 'http://localhost:5173' }));
app.use(express.json({ limit: '10mb' }));

// ─── CONSTANTS ───────────────────────────────────────────────
const NEWS_API_KEY = process.env.NEWS_API_KEY || 'df589199d35745ba87b9f65ad20b0442';
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY || '';

const DOMAIN_QUERIES = {
  EdTech: 'EdTech education technology startup',
  FinTech: 'FinTech financial technology startup',
  HealthTech: 'HealthTech digital health startup',
  'E-commerce': 'ecommerce online retail startup',
  SaaS: 'SaaS software startup funding',
  FoodTech: 'FoodTech food delivery startup',
  AgriTech: 'AgriTech agriculture technology',
  CleanTech: 'CleanTech clean energy startup',
  IoT: 'IoT Internet of Things startup',
  'AI/ML': 'artificial intelligence startup funding',
  Other: 'startup technology innovation',
};

// ─── SYNTHETIC DATA GENERATOR ────────────────────────────────
function generateSyntheticData(count = 200) {
  const cities = ['Mumbai', 'Bangalore', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Ahmedabad'];
  const industries = ['EdTech', 'FinTech', 'HealthTech', 'E-commerce', 'SaaS', 'FoodTech', 'AgriTech', 'CleanTech', 'IoT', 'AI/ML'];
  const stages = ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Growth', 'IPO'];
  const startups = [];

  for (let i = 0; i < count; i++) {
    const city = cities[Math.floor(Math.random() * cities.length)];
    const industry = industries[Math.floor(Math.random() * industries.length)];
    const stage = stages[Math.floor(Math.random() * stages.length)];
    const fundingRounds = Math.floor(Math.random() * 8) + 1;
    const totalFunding = Math.floor(Math.random() * 50000000) + 100000;
    const employees = Math.floor(Math.random() * 500) + 2;
    const successScore = Math.floor(Math.random() * 100);
    const growthRate = (Math.random() * 300 - 50).toFixed(1);
    const investorCount = Math.floor(Math.random() * 30) + 1;
    const companyAge = (Math.random() * 10 + 0.5).toFixed(1);
    const founderCount = Math.floor(Math.random() * 5) + 1;
    const isActive = Math.random() > 0.15;
    const successLabel = successScore >= 70 ? 'High' : successScore >= 40 ? 'Medium' : 'Low';

    startups.push({
      startup_id: `S${String(i + 1).padStart(4, '0')}`,
      city, industry, stage,
      funding_rounds: fundingRounds,
      total_funding_usd: totalFunding,
      employees_size_numeric: employees,
      success_score: successScore,
      growth_rate_percent: parseFloat(growthRate),
      investor_count: investorCount,
      company_age_years: parseFloat(companyAge),
      founder_count: founderCount,
      is_active: isActive,
      success_label: successLabel,
    });
  }
  return startups;
}

// ─── ML PREDICTION ───────────────────────────────────────────
function predictStartupRisk({ companyAge, founderCount, employees, fundingRounds, fundingPerRound, investorCount }) {
  const totalFunding = fundingRounds * fundingPerRound;
  let score = 0;

  // Age factor
  if (companyAge < 1) score += 10;
  else if (companyAge <= 3) score += 25;
  else if (companyAge <= 7) score += 20;
  else score += 10;

  // Team factor
  if (founderCount >= 2 && founderCount <= 4) score += 20;
  else if (founderCount === 1) score += 10;
  else score += 15;

  // Employees
  if (employees >= 10 && employees <= 100) score += 20;
  else if (employees > 100) score += 15;
  else score += 8;

  // Funding
  if (fundingRounds >= 2) score += 20;
  if (totalFunding > 1000000) score += 10;
  if (investorCount >= 3) score += 10;

  const noise = (Math.random() - 0.5) * 10;
  score = Math.max(0, Math.min(100, score + noise));

  const successProb = score / 100;
  const failureProb = (100 - score) / 100 * 0.7;
  const uncertainProb = 1 - successProb - failureProb;

  let classification, riskLevel;
  if (score >= 65) { classification = 'Success'; riskLevel = 'Low'; }
  else if (score >= 40) { classification = 'Uncertain'; riskLevel = 'Medium'; }
  else { classification = 'Failure'; riskLevel = 'High'; }

  const predictedFunding = totalFunding * (1 + successProb) * (1 + fundingRounds * 0.1);

  return {
    classification, riskLevel,
    successProbability: parseFloat(successProb.toFixed(3)),
    probabilities: {
      success: parseFloat(successProb.toFixed(3)),
      uncertain: parseFloat(Math.max(0, uncertainProb).toFixed(3)),
      failure: parseFloat(Math.max(0, failureProb).toFixed(3)),
    },
    predictedFundingUsd: Math.floor(predictedFunding),
    score: Math.round(score),
  };
}

function getProbableRisks(userInput, mlResults) {
  const risks = [];
  const { companyAge, employees, fundingRounds, founderCount, domain } = userInput;

  if (companyAge < 1) risks.push('🕐 Very early stage — high uncertainty in product-market fit validation');
  if (employees < 5) risks.push('👥 Small team size may limit execution speed and capabilities');
  if (fundingRounds === 0) risks.push('💰 No funding rounds completed — bootstrapped path carries runway risk');
  if (founderCount === 1) risks.push('🧑‍💼 Solo founder increases key-person dependency and burnout risk');
  if (mlResults.riskLevel === 'High') risks.push('📉 ML models indicate high failure probability based on comparable startups');
  if (mlResults.successProbability < 0.4) risks.push('⚠️ Below-average success probability compared to funded peers in this space');

  const domainRisks = {
    FinTech: '🏦 Heavy regulatory compliance requirements (RBI, SEBI) in FinTech space',
    HealthTech: '🏥 Healthcare regulations and data privacy (HIPAA/DPDP) are significant barriers',
    'E-commerce': '🛒 High customer acquisition cost and intense competition in e-commerce',
    EdTech: '📚 Post-COVID EdTech market consolidation — differentiation is critical',
    'AI/ML': '🤖 Rapidly evolving AI landscape requires continuous R&D investment',
  };
  if (domainRisks[domain]) risks.push(domainRisks[domain]);
  if (risks.length < 3) risks.push('📊 Market timing risk — ensure demand validation before scaling');

  return risks.slice(0, 6);
}

// ─── API ROUTES ───────────────────────────────────────────────

// Health check
app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString() }));

// Synthetic data for analytics
app.get('/api/analytics/data', (req, res) => {
  const cached = cache.get('synthetic_data');
  if (cached) return res.json(cached);
  const data = generateSyntheticData(300);
  cache.set('synthetic_data', data);
  res.json(data);
});

// News API
app.get('/api/news/:domain', async (req, res) => {
  const { domain } = req.params;
  const cacheKey = `news_${domain}_${new Date().toISOString().slice(0, 13)}`;
  const cached = cache.get(cacheKey);
  if (cached) return res.json(cached);

  const query = DOMAIN_QUERIES[domain] || domain + ' startup';
  try {
    const response = await axios.get('https://newsapi.org/v2/everything', {
      params: { q: query, sortBy: 'publishedAt', pageSize: 8, language: 'en', apiKey: NEWS_API_KEY },
      timeout: 10000,
    });
    const articles = (response.data.articles || [])
      .filter(a => a.title && a.title !== '[Removed]')
      .map(a => ({
        title: a.title,
        description: a.description || 'No description available.',
        url: a.url,
        source: a.source?.name || 'Unknown',
        published: a.publishedAt,
        image: a.urlToImage,
      }));
    cache.set(cacheKey, articles);
    res.json(articles);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ML Prediction
app.post('/api/predict', (req, res) => {
  try {
    const userInput = req.body;
    const mlResults = predictStartupRisk(userInput);
    const risks = getProbableRisks(userInput, mlResults);

    // Simulated competitors
    const competitors = Array.from({ length: 5 }, (_, i) => ({
      document: `Startup ${i + 1}: A ${userInput.domain} company with similar profile and funding trajectory.`,
      metadata: {
        industry: userInput.domain,
        funding: Math.floor(Math.random() * 10000000) + 500000,
        stage: ['Seed', 'Series A', 'Series B'][Math.floor(Math.random() * 3)],
      },
      distance: Math.random() * 0.5,
    }));

    res.json({ mlResults, risks, competitors });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// LLM Analysis via Anthropic
app.post('/api/analyze', async (req, res) => {
  const { userInput, mlResults, risks } = req.body;
  const totalFunding = userInput.fundingRounds * userInput.fundingPerRound;

  const prompt = `You are a startup analyst. Analyze this startup and provide strategic recommendations.

Startup: ${userInput.domain} — "${userInput.description}"
Age: ${userInput.companyAge} years | Team: ${userInput.founderCount} founders, ${userInput.employees} employees
Funding: $${totalFunding.toLocaleString()} over ${userInput.fundingRounds} rounds
ML Result: ${mlResults.classification} | Risk: ${mlResults.riskLevel} | Success Prob: ${(mlResults.successProbability * 100).toFixed(1)}%

Write 4-5 paragraphs covering:
1. Market opportunity and positioning
2. Strengths based on their profile
3. Key strategic risks and mitigations
4. Growth recommendations for next 12 months
5. Investor readiness assessment

Be specific, actionable, and data-driven.`;

  try {
    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      {
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1000,
        messages: [{ role: 'user', content: prompt }],
      },
      {
        headers: {
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
          'Content-Type': 'application/json',
        },
        timeout: 30000,
      }
    );
    const text = response.data.content.map(c => c.text || '').join('');
    res.json({ analysis: text });
  } catch (err) {
    const fallback = `**Strategic Analysis for ${userInput.domain} Startup**

**Market Opportunity**: The ${userInput.domain} sector presents significant growth potential. With ${userInput.companyAge} year(s) of operation and a team of ${userInput.employees} employees, you are positioned at a critical inflection point.

**Strengths**: Your ${userInput.founderCount}-founder team and ${userInput.fundingRounds} funding rounds demonstrate early investor conviction. The ${mlResults.classification} classification from our ML models suggests ${mlResults.riskLevel.toLowerCase()} risk exposure.

**Strategic Risks**: ${risks.slice(0, 2).join('. ')}. Addressing these proactively will be essential for sustainable growth.

**Growth Recommendations**: Focus on product-market fit validation, expand your investor network, and target strategic partnerships within the ${userInput.domain} ecosystem over the next 12 months.

**Investor Readiness**: With a ${(mlResults.successProbability * 100).toFixed(0)}% success probability, focus on tightening your unit economics and demonstrating repeatable growth before your next raise.`;
    res.json({ analysis: fallback });
  }
});

// Team Hierarchy via Anthropic
app.post('/api/hierarchy', async (req, res) => {
  const { userInput, mlResults } = req.body;
  const totalFunding = userInput.fundingRounds * userInput.fundingPerRound;

  const prompt = `Generate a team hierarchy JSON for a ${userInput.domain} startup with ${userInput.employees} employees.
Company: ${userInput.description}, Age: ${userInput.companyAge}yr, Funding: $${totalFunding.toLocaleString()}, ML: ${mlResults.classification}

Respond ONLY with valid JSON (no markdown) in this format:
{
  "ceo_title": "CEO & Co-Founder",
  "ceo_expertise": ["Vision", "Fundraising", "Strategy"],
  "departments": [
    {
      "name": "Engineering",
      "head_title": "CTO",
      "head_expertise": ["Architecture", "Tech Leadership"],
      "headcount": 5,
      "percentage": 40,
      "color": "#667eea",
      "roles": [{"title": "Senior Engineers", "count": 3, "expertise": ["Backend", "APIs"]}]
    }
  ],
  "key_hiring_priorities": ["First hire should be technical", "Sales after PMF"],
  "culture_values": ["Move fast", "Customer first"]
}`;

  try {
    const response = await axios.post(
      'https://api.anthropic.com/v1/messages',
      { model: 'claude-sonnet-4-20250514', max_tokens: 2000, messages: [{ role: 'user', content: prompt }] },
      {
        headers: { 'x-api-key': ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json' },
        timeout: 30000,
      }
    );
    let raw = response.data.content.map(c => c.text || '').join('').trim();
    if (raw.startsWith('```')) { raw = raw.split('```')[1]; if (raw.startsWith('json')) raw = raw.slice(4); }
    res.json(JSON.parse(raw.trim()));
  } catch (err) {
    // Fallback hierarchy
    const total = userInput.employees;
    const techCount = Math.max(1, Math.floor(total * 0.40));
    const mktCount = Math.max(1, Math.floor(total * 0.20));
    const salesCount = Math.max(1, Math.floor(total * 0.17));
    const opsCount = Math.max(1, Math.floor(total * 0.13));
    const prodCount = Math.max(1, total - techCount - mktCount - salesCount - opsCount);

    res.json({
      ceo_title: 'CEO & Co-Founder',
      ceo_expertise: ['Strategic Vision', 'Fundraising', 'Leadership'],
      departments: [
        { name: 'Engineering & Technology', head_title: 'CTO', head_expertise: ['System Architecture', 'Tech Leadership'], headcount: techCount, percentage: 40, color: '#667eea', roles: [{ title: 'Senior Engineers', count: Math.max(1, Math.floor(techCount / 2)), expertise: ['Backend', 'APIs', 'Cloud'] }, { title: 'Frontend Developers', count: Math.max(1, Math.floor(techCount / 4)), expertise: ['React', 'UX'] }] },
        { name: 'Marketing & Growth', head_title: 'CMO', head_expertise: ['Growth Strategy', 'Brand'], headcount: mktCount, percentage: 20, color: '#f093fb', roles: [{ title: 'Growth Marketers', count: Math.max(1, Math.floor(mktCount / 2)), expertise: ['SEO', 'Paid Ads'] }, { title: 'Content Creators', count: Math.max(1, mktCount - Math.floor(mktCount / 2)), expertise: ['Copywriting'] }] },
        { name: 'Sales & Business Dev', head_title: 'VP Sales', head_expertise: ['Revenue Growth', 'Partnerships'], headcount: salesCount, percentage: 17, color: '#4facfe', roles: [{ title: 'Account Executives', count: Math.max(1, Math.floor(salesCount / 2)), expertise: ['B2B Sales', 'CRM'] }] },
        { name: 'Operations & HR', head_title: 'COO', head_expertise: ['Operations', 'People Management'], headcount: opsCount, percentage: 13, color: '#43e97b', roles: [{ title: 'HR & Admin', count: Math.max(1, Math.floor(opsCount / 2)), expertise: ['Recruiting', 'Culture'] }] },
        { name: 'Product & Design', head_title: 'CPO', head_expertise: ['Product Strategy', 'UX'], headcount: prodCount, percentage: 10, color: '#fa709a', roles: [{ title: 'Product Managers', count: Math.max(1, Math.floor(prodCount / 2)), expertise: ['Roadmapping', 'Agile'] }] },
      ],
      key_hiring_priorities: [`First hires should focus on core ${userInput.domain} product development`, 'Sales/growth hiring after initial PMF', 'Build HR function when team exceeds 20'],
      culture_values: ['Move fast', 'Customer obsession', 'Radical transparency'],
    });
  }
});

// ─── PDF GENERATION ───────────────────────────────────────────
app.post('/api/generate-pdf', (req, res) => {
  const { userInput, mlResults, risks, llmAnalysis, hierarchyData } = req.body;
  const totalFunding = userInput.fundingRounds * userInput.fundingPerRound;

  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', `attachment; filename="bizgenius_report_${userInput.domain}.pdf"`);

  const doc = new PDFDocument({ margin: 50, size: 'A4' });
  doc.pipe(res);

  // Cover
  doc.rect(0, 0, doc.page.width, 180).fill('#667eea');
  doc.fillColor('white').fontSize(32).font('Helvetica-Bold').text('BizGenius', 50, 50);
  doc.fontSize(16).font('Helvetica').text('Startup Intelligence Report', 50, 95);
  doc.fontSize(11).text(`Generated: ${new Date().toLocaleDateString('en-IN', { dateStyle: 'long' })}`, 50, 125);
  doc.fillColor('#1f2937');

  // Company Info
  doc.moveDown(3);
  doc.fontSize(18).font('Helvetica-Bold').fillColor('#667eea').text('Company Overview', 50, 210);
  doc.moveTo(50, 233).lineTo(545, 233).strokeColor('#667eea').lineWidth(2).stroke();
  doc.fillColor('#1f2937').fontSize(11).font('Helvetica');

  const info = [
    ['Domain', userInput.domain], ['Description', userInput.description],
    ['Company Age', `${userInput.companyAge} years`], ['Founders', userInput.founderCount],
    ['Employees', userInput.employees], ['Funding Rounds', userInput.fundingRounds],
    ['Total Funding', `$${totalFunding.toLocaleString()}`],
  ];
  let y = 245;
  info.forEach(([k, v]) => {
    doc.font('Helvetica-Bold').text(`${k}:`, 55, y, { continued: true });
    doc.font('Helvetica').text(`  ${v}`, { continued: false });
    y += 18;
  });

  // ML Results
  y += 20;
  doc.fontSize(18).font('Helvetica-Bold').fillColor('#667eea').text('ML Predictions', 50, y);
  y += 25;
  doc.moveTo(50, y).lineTo(545, y).strokeColor('#667eea').lineWidth(2).stroke();
  y += 15;

  const mlInfo = [
    ['Classification', mlResults.classification],
    ['Risk Level', mlResults.riskLevel],
    ['Success Probability', `${(mlResults.successProbability * 100).toFixed(1)}%`],
    ['Predicted Next Round', `$${mlResults.predictedFundingUsd?.toLocaleString() || 'N/A'}`],
  ];
  doc.fillColor('#1f2937').fontSize(11);
  mlInfo.forEach(([k, v]) => {
    doc.font('Helvetica-Bold').text(`${k}:`, 55, y, { continued: true });
    doc.font('Helvetica').text(`  ${v}`);
    y += 18;
  });

  // Risks
  y += 20;
  doc.addPage();
  doc.fontSize(18).font('Helvetica-Bold').fillColor('#667eea').text('Identified Risks', 50, 50);
  doc.moveTo(50, 73).lineTo(545, 73).strokeColor('#667eea').lineWidth(2).stroke();
  doc.fillColor('#1f2937').fontSize(11).font('Helvetica');
  let ry = 85;
  risks.forEach((risk, i) => {
    doc.text(`${i + 1}. ${risk}`, 55, ry, { width: 490 });
    ry += 30;
  });

  // AI Analysis
  ry += 20;
  doc.fontSize(18).font('Helvetica-Bold').fillColor('#667eea').text('AI Strategic Analysis', 50, ry);
  ry += 25;
  doc.moveTo(50, ry).lineTo(545, ry).strokeColor('#667eea').lineWidth(2).stroke();
  ry += 15;
  doc.fillColor('#1f2937').fontSize(10).font('Helvetica')
    .text(llmAnalysis || 'Analysis not available.', 55, ry, { width: 490, lineGap: 4 });

  // Team Hierarchy
  if (hierarchyData) {
    doc.addPage();
    doc.fontSize(18).font('Helvetica-Bold').fillColor('#667eea').text('Team Hierarchy', 50, 50);
    doc.moveTo(50, 73).lineTo(545, 73).strokeColor('#667eea').lineWidth(2).stroke();
    let hy = 85;
    doc.fillColor('#1f2937').fontSize(11).font('Helvetica-Bold').text(`CEO: ${hierarchyData.ceo_title}`, 55, hy);
    hy += 25;
    (hierarchyData.departments || []).forEach(dept => {
      doc.fontSize(12).font('Helvetica-Bold').fillColor('#667eea').text(`${dept.name} — ${dept.headcount} people (${dept.percentage}%)`, 55, hy);
      hy += 18;
      doc.fillColor('#555').fontSize(10).font('Helvetica').text(`Head: ${dept.head_title}`, 70, hy);
      hy += 15;
      (dept.roles || []).forEach(role => {
        doc.text(`• ${role.title} (${role.count}) — ${role.expertise?.join(', ')}`, 75, hy);
        hy += 14;
      });
      hy += 10;
      if (hy > 750) { doc.addPage(); hy = 50; }
    });

    if (hierarchyData.key_hiring_priorities?.length) {
      hy += 10;
      doc.fontSize(13).font('Helvetica-Bold').fillColor('#667eea').text('Key Hiring Priorities', 55, hy);
      hy += 18;
      hierarchyData.key_hiring_priorities.forEach((p, i) => {
        doc.fillColor('#1f2937').fontSize(10).font('Helvetica').text(`${i + 1}. ${p}`, 65, hy, { width: 480 });
        hy += 20;
      });
    }
  }

  // Footer
  doc.fontSize(9).fillColor('#888').text('Powered by BizGenius — Startup Intelligence Platform', 50, doc.page.height - 40, { align: 'center' });
  doc.end();
});

// ─── PPTX GENERATION ─────────────────────────────────────────
app.post('/api/generate-pptx', async (req, res) => {
  const { userInput, mlResults, risks, llmAnalysis, hierarchyData } = req.body;
  const totalFunding = userInput.fundingRounds * userInput.fundingPerRound;
  const companyName = (userInput.description?.split(' ').slice(0, 3).join(' ') || 'Your Startup');

  try {
    const pptx = new PptxGenJS();
    pptx.layout = 'LAYOUT_WIDE';
    pptx.title = 'BizGenius Pitch Deck';

    const PURPLE = '667eea';
    const DARK = '1f2937';
    const WHITE = 'FFFFFF';
    const PINK = 'f093fb';
    const BLUE = '4facfe';
    const GREEN = '43e97b';

    // Slide 1 — Cover
    const slide1 = pptx.addSlide();
    slide1.background = { fill: PURPLE };
    slide1.addText(companyName, { x: 0.5, y: 1.5, w: '90%', h: 1.5, fontSize: 54, bold: true, color: WHITE, align: 'center' });
    slide1.addText(`Disrupting ${userInput.domain}`, { x: 0.5, y: 3.2, w: '90%', h: 0.8, fontSize: 24, color: 'CCDDFF', align: 'center' });
    slide1.addText(`Success Probability: ${(mlResults.successProbability * 100).toFixed(0)}%  |  Risk: ${mlResults.riskLevel}`, { x: 0.5, y: 4.2, w: '90%', h: 0.6, fontSize: 16, color: 'AABCFF', align: 'center' });
    slide1.addText('Powered by BizGenius', { x: 0.5, y: 6.8, w: '90%', h: 0.4, fontSize: 12, color: 'AABCFF', align: 'center', italic: true });

    // Slide 2 — Company Overview
    const slide2 = pptx.addSlide();
    slide2.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: PURPLE } });
    slide2.addText('Company Overview', { x: 0.4, y: 0.2, w: '90%', h: 0.8, fontSize: 28, bold: true, color: WHITE });
    const overviewData = [
      [{ text: 'Metric', options: { bold: true, fill: { color: PURPLE }, color: WHITE } }, { text: 'Details', options: { bold: true, fill: { color: PURPLE }, color: WHITE } }],
      ['Domain / Industry', userInput.domain],
      ['Idea / Description', userInput.description?.slice(0, 80) || ''],
      ['Company Age', `${userInput.companyAge} years`],
      ['Founding Team', `${userInput.founderCount} founders`],
      ['Team Size', `${userInput.employees} employees`],
      ['Funding Rounds', `${userInput.fundingRounds} rounds`],
      ['Total Funding Raised', `$${totalFunding.toLocaleString()}`],
      ['Investors', `${userInput.investorCount} investors`],
    ];
    slide2.addTable(overviewData, { x: 0.5, y: 1.4, w: 12, colW: [3, 9], fontSize: 13, border: { pt: 1, color: 'DDDDDD' }, autoPage: false });

    // Slide 3 — ML Predictions
    const slide3 = pptx.addSlide();
    slide3.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: PURPLE } });
    slide3.addText('AI/ML Predictions', { x: 0.4, y: 0.2, w: '90%', h: 0.8, fontSize: 28, bold: true, color: WHITE });

    const predCards = [
      { label: 'Classification', value: mlResults.classification, color: mlResults.classification === 'Success' ? '28a745' : mlResults.classification === 'Failure' ? 'dc3545' : 'ffc107' },
      { label: 'Risk Level', value: mlResults.riskLevel, color: mlResults.riskLevel === 'Low' ? '28a745' : mlResults.riskLevel === 'High' ? 'dc3545' : 'ffc107' },
      { label: 'Success Probability', value: `${(mlResults.successProbability * 100).toFixed(1)}%`, color: PURPLE },
      { label: 'Predicted Next Round', value: `$${(mlResults.predictedFundingUsd / 1000000).toFixed(2)}M`, color: PURPLE },
    ];
    predCards.forEach((card, i) => {
      const x = 0.5 + (i % 2) * 6.5;
      const y = 1.5 + Math.floor(i / 2) * 2.2;
      slide3.addShape(pptx.ShapeType.rect, { x, y, w: 6, h: 1.8, fill: { color: 'F8F9FF' }, line: { color: card.color, pt: 2 } });
      slide3.addText(card.label, { x: x + 0.2, y: y + 0.2, w: 5.6, h: 0.5, fontSize: 13, color: '666666' });
      slide3.addText(card.value, { x: x + 0.2, y: y + 0.7, w: 5.6, h: 0.9, fontSize: 26, bold: true, color: card.color });
    });

    // Slide 4 — Risks
    const slide4 = pptx.addSlide();
    slide4.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: 'dc3545' } });
    slide4.addText('Key Risk Factors', { x: 0.4, y: 0.2, w: '90%', h: 0.8, fontSize: 28, bold: true, color: WHITE });
    const riskRows = risks.map((r, i) => [{ text: `${i + 1}`, options: { bold: true, align: 'center', color: WHITE, fill: { color: 'dc3545' } } }, { text: r }]);
    slide4.addTable([
      [{ text: '#', options: { bold: true, fill: { color: '1f2937' }, color: WHITE } }, { text: 'Risk Factor', options: { bold: true, fill: { color: '1f2937' }, color: WHITE } }],
      ...riskRows
    ], { x: 0.5, y: 1.4, w: 12, colW: [0.8, 11.2], fontSize: 12, border: { pt: 1, color: 'DDDDDD' } });

    // Slide 5 — Team Hierarchy
    if (hierarchyData) {
      const slide5 = pptx.addSlide();
      slide5.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: PURPLE } });
      slide5.addText('Team Hierarchy & Distribution', { x: 0.4, y: 0.2, w: '90%', h: 0.8, fontSize: 28, bold: true, color: WHITE });
      slide5.addText(`CEO: ${hierarchyData.ceo_title}`, { x: 4, y: 1.4, w: 5, h: 0.7, fontSize: 16, bold: true, color: WHITE, fill: { color: PURPLE }, align: 'center' });

      const deptColors = [PURPLE, PINK, BLUE, GREEN, 'fa709a'];
      const depts = hierarchyData.departments || [];
      depts.slice(0, 5).forEach((dept, i) => {
        const col = i % 3;
        const row = Math.floor(i / 3);
        const x = 0.3 + col * 4.3;
        const y = 2.4 + row * 2.5;
        const color = deptColors[i] || PURPLE;
        slide5.addShape(pptx.ShapeType.rect, { x, y, w: 4, h: 0.55, fill: { color } });
        slide5.addText(`${dept.name} (${dept.headcount})`, { x, y: y + 0.05, w: 4, h: 0.45, fontSize: 11, bold: true, color: WHITE, align: 'center' });
        slide5.addShape(pptx.ShapeType.rect, { x, y: y + 0.55, w: 4, h: 1.6, fill: { color: 'F8F9FF' }, line: { color, pt: 1 } });
        const roleText = (dept.roles || []).slice(0, 3).map(r => `• ${r.title} (${r.count})`).join('\n');
        slide5.addText(roleText, { x: x + 0.1, y: y + 0.65, w: 3.8, h: 1.4, fontSize: 9, color: DARK });
      });
    }

    // Slide 6 — AI Analysis
    const slide6 = pptx.addSlide();
    slide6.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: PURPLE } });
    slide6.addText('AI Strategic Analysis', { x: 0.4, y: 0.2, w: '90%', h: 0.8, fontSize: 28, bold: true, color: WHITE });
    slide6.addText((llmAnalysis || 'Analysis not available').slice(0, 800), {
      x: 0.5, y: 1.4, w: 12.2, h: 5.5, fontSize: 11, color: DARK, wrap: true, valign: 'top'
    });

    // Slide 7 — Thank You
    const slide7 = pptx.addSlide();
    slide7.background = { fill: DARK };
    slide7.addText('Thank You', { x: 0.5, y: 2.5, w: '90%', h: 1.2, fontSize: 48, bold: true, color: WHITE, align: 'center' });
    slide7.addText(`${companyName} — Powered by BizGenius`, { x: 0.5, y: 4, w: '90%', h: 0.6, fontSize: 18, color: '667eea', align: 'center' });

    const pptxBuffer = await pptx.write({ outputType: 'nodebuffer' });
    res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation');
    res.setHeader('Content-Disposition', `attachment; filename="bizgenius_pitch_${userInput.domain}.pptx"`);
    res.send(pptxBuffer);
  } catch (err) {
    console.error('PPTX error:', err);
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`🚀 BizGenius API running on http://localhost:${PORT}`));