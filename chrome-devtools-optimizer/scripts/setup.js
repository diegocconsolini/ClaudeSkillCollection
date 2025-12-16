#!/usr/bin/env node
/**
 * Chrome DevTools Optimizer - Interactive Setup
 * Configures Gemini API key for screenshot processing
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const CONFIG_DIR = path.join(require('os').homedir(), '.config', 'chrome-devtools-optimizer');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

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
  console.log('\nSetup complete! You can now use:');
  console.log('  node scripts/process-screenshot.js <image_file_or_base64>');
  console.log('  node scripts/test-connection.js');

  rl.close();
}

main().catch(err => {
  console.error('Setup failed:', err.message);
  rl.close();
  process.exit(1);
});
