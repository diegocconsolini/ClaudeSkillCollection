#!/usr/bin/env node
/**
 * Chrome DevTools Optimizer - Connection Test
 * Verifies Gemini API configuration is working
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const CONFIG_DIR = path.join(require('os').homedir(), '.config', 'chrome-devtools-optimizer');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

function testAPI(config) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      contents: [{
        parts: [{ text: 'Reply with exactly: OK' }]
      }],
      generationConfig: {
        temperature: 0,
        maxOutputTokens: 10
      }
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

async function main() {
  console.log('\n===========================================');
  console.log('  Chrome DevTools Optimizer - Connection Test');
  console.log('===========================================\n');

  // Check config exists
  console.log('1. Checking configuration...');
  if (!fs.existsSync(CONFIG_FILE)) {
    console.log('   ✗ Config not found');
    console.log('\n   Run setup first:');
    console.log('   node chrome-devtools-optimizer/scripts/setup.js\n');
    process.exit(1);
  }
  console.log('   ✓ Config found:', CONFIG_FILE);

  // Load config
  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  const maskedKey = config.geminiApiKey.slice(0, 8) + '...' + config.geminiApiKey.slice(-4);
  console.log('   ✓ API Key:', maskedKey);
  console.log('   ✓ Model:', config.model);

  // Test API
  console.log('\n2. Testing Gemini API connection...');
  try {
    const result = await testAPI(config);
    console.log('   ✓ API responded:', result.response?.trim());
    console.log('\n==========================================');
    console.log('  All tests passed! Ready to use.');
    console.log('==========================================\n');
  } catch (error) {
    console.log('   ✗ API Error:', error.message);
    console.log('\n   Possible issues:');
    console.log('   - Invalid API key');
    console.log('   - API quota exceeded');
    console.log('   - Network connectivity');
    console.log('\n   Get a new key at: https://aistudio.google.com/apikey\n');
    process.exit(1);
  }
}

main();
