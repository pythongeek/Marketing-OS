const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync('tmp/all-final-jobs.json', 'utf8'));
const base = 'AgenticMarketingPro-Vault/01-Clients/agenticmarketingpro/masterplan-deliverables/';

const fileMap = {
  'social-media-manager': {
    'Social Media Strategy': ['09-social', '09-social-media-strategy.md'],
    'X Twitter': ['09-social', '09-social-media-strategy.md'],
  },
  'paid-ads-manager': {
    'Search Ads': ['10-search-ads', '10-search-ads-strategy.md'],
    'Meta LinkedIn': ['11-other-ads', '11-other-channel-ads.md'],
    'Google Ads': ['10-search-ads', '10-search-ads-strategy.md'],
  },
  'content-strategist': {
    'Unique Marketing': ['12-unique-methods', '12-unique-marketing-methods.md'],
    '90-Day': ['14-90day-timeline', '14-90day-launch-timeline.md'],
  },
  'competitor-intelligence': {
    'Competitor Outranking': ['13-competitor-outrank', '13-competitor-outranking.md'],
  }
};

let saved = 0;
jobs.forEach(j => {
  if (!j.result || !j.result.content) return;
  const skill = j.skill_slug;
  const topic = j.payload.topic || '';
  
  let dir, file;
  
  if (skill === 'social-media-manager' && topic.includes('Social Media Strategy')) {
    dir = '09-social'; file = '09-social-media-strategy.md';
  } else if (skill === 'paid-ads-manager' && topic.includes('Search Ads')) {
    dir = '10-search-ads'; file = '10-search-ads-strategy.md';
  } else if (skill === 'paid-ads-manager' && topic.includes('Other Channel')) {
    dir = '11-other-ads'; file = '11-other-channel-ads.md';
  } else if (skill === 'content-strategist' && topic.includes('Unique Marketing')) {
    dir = '12-unique-methods'; file = '12-unique-marketing-methods.md';
  } else if (skill === 'competitor-intelligence') {
    dir = '13-competitor-outrank'; file = '13-competitor-outranking.md';
  } else if (skill === 'content-strategist' && topic.includes('90-Day')) {
    dir = '14-90day-timeline'; file = '14-90day-launch-timeline.md';
  } else {
    return;
  }
  
  fs.writeFileSync(base + dir + '/' + file, j.result.content);
  console.log('Saved:', skill, '->', file, j.result.content.length, 'chars');
  saved++;
});

console.log('\nTotal saved in this batch:', saved);
