#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Get the directory where this package is installed
const packageDir = path.dirname(__dirname);

// Spawn the Python MCP server
const pythonProcess = spawn('python', ['-m', 'devops_extended.mcp'], {
  cwd: packageDir,
  stdio: 'inherit',
  env: process.env
});

pythonProcess.on('error', (error) => {
  console.error('Failed to start MCP server:', error);
  process.exit(1);
});

pythonProcess.on('exit', (code) => {
  process.exit(code || 0);
});

// Handle cleanup on termination
process.on('SIGINT', () => {
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});
