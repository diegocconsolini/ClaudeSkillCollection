#!/usr/bin/env node
/**
 * Chrome DevTools Optimizer - Screenshot Processor
 * Uses Gemini Flash to analyze screenshots and return text summaries
 *
 * Usage:
 *   node process-screenshot.js <image_file>           # Process a file
 *   node process-screenshot.js <base64_string>        # Process base64 data
 *   node process-screenshot.js --prompt "custom"      # Custom analysis prompt
 *   echo <base64> | node process-screenshot.js -      # Read from stdin
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const CONFIG_DIR = path.join(require('os').homedir(), '.config', 'chrome-devtools-optimizer');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

// Default analysis prompt optimized for web UI screenshots
const DEFAULT_PROMPT = `Analyze this web page screenshot concisely. Include:
1. Page type/purpose (login, dashboard, form, etc.)
2. Key UI elements visible (buttons, forms, menus, etc.)
3. Current state (loaded, error, loading, etc.)
4. Any visible text content (headings, labels, messages)
5. Notable visual issues if any (alignment, overflow, etc.)

Be brief and factual. Focus on what's actionable for web testing.`;

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('Error: Not configured. Run setup first:');
    console.error('  node chrome-devtools-optimizer/scripts/setup.js');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
}

function isBase64(str) {
  if (str.length < 100) return false;
  const base64Regex = /^[A-Za-z0-9+/=]+$/;
  return base64Regex.test(str.replace(/\s/g, ''));
}

function getImageData(input) {
  // Check if it's a file path
  if (fs.existsSync(input)) {
    const ext = path.extname(input).toLowerCase();
    const mimeTypes = {
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.webp': 'image/webp'
    };
    const mimeType = mimeTypes[ext] || 'image/png';
    const data = fs.readFileSync(input).toString('base64');
    return { data, mimeType };
  }

  // Check if it's base64 data
  if (isBase64(input)) {
    // Try to detect mime type from base64 header
    let mimeType = 'image/png';
    if (input.startsWith('/9j/')) mimeType = 'image/jpeg';
    if (input.startsWith('iVBOR')) mimeType = 'image/png';
    if (input.startsWith('R0lGOD')) mimeType = 'image/gif';
    return { data: input, mimeType };
  }

  // Check if it's a data URL
  const dataUrlMatch = input.match(/^data:([^;]+);base64,(.+)$/);
  if (dataUrlMatch) {
    return { data: dataUrlMatch[2], mimeType: dataUrlMatch[1] };
  }

  throw new Error('Invalid input: not a file path, base64 string, or data URL');
}

function callGeminiAPI(config, imageData, prompt) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      contents: [{
        parts: [
          { text: prompt },
          {
            inline_data: {
              mime_type: imageData.mimeType,
              data: imageData.data
            }
          }
        ]
      }],
      generationConfig: {
        temperature: 0.2,
        maxOutputTokens: 1024
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
          if (!text) {
            reject(new Error('No response text from Gemini'));
            return;
          }
          resolve(text);
        } catch (e) {
          reject(new Error(`Failed to parse response: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data.trim()));
  });
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
Chrome DevTools Optimizer - Screenshot Processor

Usage:
  node process-screenshot.js <image_file>           Process an image file
  node process-screenshot.js <base64_string>        Process base64 data
  node process-screenshot.js - < file.txt           Read base64 from stdin
  node process-screenshot.js --prompt "..." <img>   Custom analysis prompt

Options:
  --prompt, -p    Custom prompt for image analysis
  --json, -j      Output as JSON
  --help, -h      Show this help

Examples:
  node process-screenshot.js screenshot.png
  node process-screenshot.js --prompt "Find all buttons" page.png
  node process-screenshot.js -j screenshot.png
`);
    process.exit(0);
  }

  // Parse arguments
  let customPrompt = null;
  let jsonOutput = false;
  let input = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--prompt' || args[i] === '-p') {
      customPrompt = args[++i];
    } else if (args[i] === '--json' || args[i] === '-j') {
      jsonOutput = true;
    } else if (args[i] === '-') {
      input = await readStdin();
    } else if (!input) {
      input = args[i];
    }
  }

  if (!input) {
    console.error('Error: No input provided');
    process.exit(1);
  }

  const config = loadConfig();
  const prompt = customPrompt || DEFAULT_PROMPT;

  try {
    const imageData = getImageData(input);
    const analysis = await callGeminiAPI(config, imageData, prompt);

    if (jsonOutput) {
      console.log(JSON.stringify({
        success: true,
        analysis,
        model: config.model,
        promptUsed: prompt !== DEFAULT_PROMPT ? 'custom' : 'default'
      }, null, 2));
    } else {
      console.log(analysis);
    }
  } catch (error) {
    if (jsonOutput) {
      console.log(JSON.stringify({
        success: false,
        error: error.message
      }, null, 2));
    } else {
      console.error('Error:', error.message);
    }
    process.exit(1);
  }
}

main();
