const fs = require('fs');

const jobs = JSON.parse(fs.readFileSync('tmp/seo-ops-all.json', 'utf8'));
const base = 'AgenticMarketingPro-Vault/01-Clients/agenticmarketingpro/seo-ops/';

// Ensure directories exist
const dirs = ['01-content-refresh', '02-gsc-operations', '03-bing-operations', '04-technical-health', '05-advanced-tactics', '06-master-cadence'];
dirs.forEach(d => {
  try { fs.mkdirSync(base + d, { recursive: true }); } catch(e) {}
});

let saved = 0;

jobs.forEach(j => {
  if (!j.result || !j.result.content) return;
  
  const skill = j.skill_slug;
  const topic = j.payload.topic || '';
  let filepath;
  
  // Map jobs to files based on topic content
  if (topic.includes('Content Refresh')) {
    filepath = base + '01-content-refresh/01-content-refresh-queue.md';
  } else if (topic.includes('Google Search Console')) {
    filepath = base + '02-gsc-operations/02-gsc-weekly-monthly-ops.md';
  } else if (topic.includes('Bing Webmaster')) {
    filepath = base + '03-bing-operations/03-bing-wmt-indexnow.md';
  } else if (topic.includes('Technical Health')) {
    filepath = base + '04-technical-health/04-technical-health-ops.md';
  } else if (topic.includes('Lesser-Known') || topic.includes('Advanced')) {
    filepath = base + '05-advanced-tactics/05-advanced-seo-tactics.md';
  } else if (topic.includes('Cadence') || topic.includes('Calendar')) {
    filepath = base + '06-master-cadence/06-master-ops-cadence.md';
  } else {
    return; // Skip non-SEO-ops jobs
  }
  
  fs.writeFileSync(filepath, j.result.content);
  console.log('Saved:', filepath.replace(base, ''), '-', j.result.content.length, 'chars');
  saved++;
});

console.log('\nTotal SEO Ops deliverables saved:', saved);
