/**
 * Test environment variable loading
 */
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');
console.log('Looking for .env at:', envPath);
console.log('File exists:', fs.existsSync(envPath));

if (fs.existsSync(envPath)) {
  const content = fs.readFileSync(envPath, 'utf8');
  console.log('\n.env file content (first 200 chars):');
  console.log(content.slice(0, 200));
}

// Load manually
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  for (const line of envContent.split('\n')) {
    const match = line.match(/^([^#=]+)=(.*)$/);
    if (match && !process.env[match[1]]) {
      process.env[match[1]] = match[2].trim();
    }
  }
}

console.log('\nEnvironment variables after loading:');
console.log('SUPABASE_URL:', process.env.SUPABASE_URL ? 'SET' : 'NOT SET');
console.log('SUPABASE_SERVICE_ROLE_KEY:', process.env.SUPABASE_SERVICE_ROLE_KEY ? 'SET' : 'NOT SET');
console.log('MINIMAX_API_KEY:', process.env.MINIMAX_API_KEY ? 'SET (' + process.env.MINIMAX_API_KEY.slice(0, 20) + '...)' : 'NOT SET');
console.log('OPENAI_API_KEY:', process.env.OPENAI_API_KEY ? 'SET' : 'NOT SET');
