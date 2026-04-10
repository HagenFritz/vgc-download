#!/usr/bin/env node

import fs from 'fs'
import path from 'path'
import os from 'os'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const packageRoot = path.resolve(__dirname, '..')
const claudeDir = path.join(os.homedir(), '.claude')
const SKILLS_DIR = path.join(claudeDir, 'skills')
const AGENTS_DIR = path.join(claudeDir, 'agents')
const MCP_CONFIG = path.join(claudeDir, 'mcp.json')
const MCP_SERVER_NAME = 'vgc-download'

function copyDirRecursive(src, dest) {
  fs.mkdirSync(dest, { recursive: true })
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name)
    const destPath = path.join(dest, entry.name)
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath)
    } else {
      fs.copyFileSync(srcPath, destPath)
    }
  }
}

function installSkills() {
  const skillsSource = path.join(packageRoot, 'skills')
  if (!fs.existsSync(skillsSource)) return []

  const copied = []
  for (const name of fs.readdirSync(skillsSource)) {
    const src = path.join(skillsSource, name)
    if (!fs.statSync(src).isDirectory()) continue
    copyDirRecursive(src, path.join(SKILLS_DIR, name))
    copied.push(name)
  }
  return copied
}

function installAgents() {
  const agentsSource = path.join(packageRoot, 'agents')
  if (!fs.existsSync(agentsSource)) return []

  const copied = []
  for (const category of fs.readdirSync(agentsSource)) {
    const src = path.join(agentsSource, category)
    if (!fs.statSync(src).isDirectory()) continue
    // Skip empty directories
    if (fs.readdirSync(src).length === 0) continue
    copyDirRecursive(src, path.join(AGENTS_DIR, category))
    copied.push(category)
  }
  return copied
}

function installMcp() {
  const serverScript = path.join(packageRoot, 'mcp-server', 'server.py')
  if (!fs.existsSync(serverScript)) return false

  let config = { mcpServers: {} }
  if (fs.existsSync(MCP_CONFIG)) {
    config = JSON.parse(fs.readFileSync(MCP_CONFIG, 'utf-8'))
    if (!config.mcpServers) config.mcpServers = {}
  }

  config.mcpServers[MCP_SERVER_NAME] = {
    command: 'uv',
    args: ['run', '--directory', packageRoot, 'python', serverScript]
  }

  fs.writeFileSync(MCP_CONFIG, JSON.stringify(config, null, 2) + '\n')
  return true
}

function uninstallSkills() {
  const skillsSource = path.join(packageRoot, 'skills')
  if (!fs.existsSync(skillsSource)) return []

  const removed = []
  for (const name of fs.readdirSync(skillsSource)) {
    const dir = path.join(SKILLS_DIR, name)
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true })
      removed.push(name)
    }
  }
  return removed
}

function uninstallAgents() {
  const agentsSource = path.join(packageRoot, 'agents')
  if (!fs.existsSync(agentsSource)) return []

  const removed = []
  for (const category of fs.readdirSync(agentsSource)) {
    const dir = path.join(AGENTS_DIR, category)
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true })
      removed.push(category)
    }
  }
  return removed
}

function uninstallMcp() {
  if (!fs.existsSync(MCP_CONFIG)) return false

  const config = JSON.parse(fs.readFileSync(MCP_CONFIG, 'utf-8'))
  if (!config.mcpServers || !config.mcpServers[MCP_SERVER_NAME]) return false

  delete config.mcpServers[MCP_SERVER_NAME]
  fs.writeFileSync(MCP_CONFIG, JSON.stringify(config, null, 2) + '\n')
  return true
}

function install() {
  console.log('\nvgc-download — VGC coaching plugin for Claude Code\n')

  const skills = installSkills()
  if (skills.length) {
    console.log(`Skills: copied ${skills.length} — ${skills.join(', ')}`)
  } else {
    console.log('Skills: none found')
  }

  const agents = installAgents()
  if (agents.length) {
    console.log(`Agents: copied ${agents.length} category(s) — ${agents.join(', ')}`)
  } else {
    console.log('Agents: none to install')
  }

  const mcp = installMcp()
  if (mcp) {
    console.log(`MCP: registered "${MCP_SERVER_NAME}" in ${MCP_CONFIG}`)
  } else {
    console.log('MCP: no server.py found, skipped')
  }

  console.log('\nRestart Claude Code for changes to take effect.\n')
}

function uninstall() {
  console.log('\nvgc-download — removing plugin\n')

  const skills = uninstallSkills()
  console.log(`Skills: removed ${skills.length} — ${skills.join(', ') || 'none'}`)

  const agents = uninstallAgents()
  console.log(`Agents: removed ${agents.length} — ${agents.join(', ') || 'none'}`)

  const mcp = uninstallMcp()
  console.log(`MCP: ${mcp ? 'removed from config' : 'not found in config'}`)

  console.log('\nRestart Claude Code for changes to take effect.\n')
}

const command = process.argv[2]

switch (command) {
  case 'install':
    install()
    break
  case 'uninstall':
    uninstall()
    break
  default:
    console.log(`vgc-download — VGC coaching plugin for Claude Code

Usage:
  npx vgc-download install      Install skills, agents, and MCP server
  npx vgc-download uninstall    Remove all installed components
`)
    process.exit(command ? 1 : 0)
}
