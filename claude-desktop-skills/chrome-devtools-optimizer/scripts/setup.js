#!/usr/bin/env node
/**
 * Chrome DevTools Optimizer - Interactive Setup
 * Configures Gemini API key for screenshot processing
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const https = require('https');

const CONFIG_DIR = path.join(require('os').homedir(), '.config', 'chrome-devtools-optimizer');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

// Test API connection
function testAPI(config) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      contents: [{ parts: [{ text: 'Reply with exactly: OK' }] }],
      generationConfig: { temperature: 0, maxOutputTokens: 10 }
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      port: 443,
      path: `/v1beta/models/${config.model}:generateContent?key=${config.geminiApiKey}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.error) {
            reject(new Error(response.error.message));
            return;
          }
          const text = response.candidates?.[0]?.content?.parts?.[0]?.text;
          resolve({ status: res.statusCode, response: text });
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise(resolve => rl.question(prompt, resolve));
}

async function main() {
  console.log('\n===========================================');
  console.log('  Chrome DevTools Optimizer - Setup');
  console.log('===========================================\n');

  // Check if already configured
  if (fs.existsSync(CONFIG_FILE)) {
    const existing = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    if (existing.geminiApiKey) {
      const masked = existing.geminiApiKey.slice(0, 8) + '...' + existing.geminiApiKey.slice(-4);
      console.log(`Existing configuration found.`);
      console.log(`API Key: ${masked}\n`);

      const reconfigure = await question('Reconfigure? (y/N): ');
      if (reconfigure.toLowerCase() !== 'y') {
        console.log('\nSetup cancelled. Existing configuration kept.');
        rl.close();
        return;
      }
    }
  }

  console.log('This plugin uses Google Gemini Flash for efficient screenshot analysis.');
  console.log('Gemini Flash is ~25x cheaper than Claude vision for image processing.\n');
  console.log('Free tier: 15 requests/min, 1M tokens/day');
  console.log('Get your API key at: https://aistudio.google.com/apikey\n');

  const apiKey = await question('Enter your Gemini API Key: ');

  if (!apiKey || apiKey.trim().length < 10) {
    console.log('\nInvalid API key. Setup cancelled.');
    rl.close();
    return;
  }

  // Create config directory
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }

  // Save config
  const config = {
    geminiApiKey: apiKey.trim(),
    model: 'gemini-2.0-flash-exp',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));

  console.log('\n✓ Configuration saved to:', CONFIG_FILE);

  // Auto-test the connection
  console.log('\n🔄 Testing API connection...');
  try {
    const result = await testAPI(config);
    console.log('✅ API test passed! Response:', result.response?.trim());
    console.log('\n==========================================');
    console.log('  Setup complete! Ready to use.');
    console.log('==========================================');
    console.log('\nUsage:');
    console.log('  node scripts/process-screenshot.js <image_file_or_base64>');
  } catch (error) {
    console.log('❌ API test failed:', error.message);
    console.log('\nPossible issues:');
    console.log('  - Invalid API key');
    console.log('  - API quota exceeded');
    console.log('  - Network connectivity');
    console.log('\nGet a new key at: https://aistudio.google.com/apikey');
    console.log('Then run: node scripts/setup.js');
  }

  rl.close();
}

main().catch(err => {
  console.error('Setup failed:', err.message);
  rl.close();
  process.exit(1);
});
