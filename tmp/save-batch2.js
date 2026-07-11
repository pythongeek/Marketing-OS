const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync('tmp/all-jobs-batch2.json', 'utf8'));
const base = 'AgenticMarketingPro-Vault/01-Clients/agenticmarketingpro/masterplan-deliverables/';

jobs.forEach(j => {
  if (!j.result || !j.result.content) return;
  const skill = j.skill_slug;
  const topic = j.payload.topic || '';
  let dir, file;
  
  if (skill === 'content-strategist') {
    if (topic.includes('AI Visibility')) {
      dir = '05-ai-content'; file = '05-ai-visibility-content.md';
    } else if (topic.includes('Traditional Search')) {
      dir = '06-search-content'; file = '06-search-content-plan.md';
    } else {
      return;
    }
  } else if (skill === 'social-media-manager') {
    if (topic.includes('LinkedIn')) {
      dir = '07-linkedin'; file = '07-linkedin-lead-gen.md';
    } else if (topic.includes('Reddit')) {
      dir = '08-reddit'; file = '08-reddit-strategy.md';
    } else {
      return;
    }
  } else {
    return;
  }
  
  fs.writeFileSync(base + dir + '/' + file, j.result.content);
  console.log('Saved:', skill, file, j.result.content.length, 'chars');
});
