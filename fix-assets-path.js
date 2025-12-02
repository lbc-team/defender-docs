#!/usr/bin/env node

/**
 * 修复构建产物中的静态资源路径
 * 将 /_/ 替换为自定义路径前缀
 */

const fs = require('fs');
const path = require('path');

// 默认配置
const DEFAULT_CONFIG = {
  buildDir: 'build/site',
  pathMappings: {
    '/_/': '/docs/openzeppelin/CommunityContracts/_/'
  },
  fileExtensions: ['.html', '.js', '.css', '.xml']
};

// 加载配置
function loadConfig() {
  const configPath = path.resolve('assets-config.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      return { ...DEFAULT_CONFIG, ...config };
    } catch (error) {
      console.warn(`配置文件读取失败，使用默认配置: ${error.message}`);
    }
  }
  return DEFAULT_CONFIG;
}

const config = loadConfig();

function processDirectory(dir) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      processDirectory(filePath);
    } else if (config.fileExtensions.some(ext => file.endsWith(ext))) {
      processFile(filePath);
    }
  }
}

function processFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // 应用路径映射规则，避免重复替换
    for (const [oldPath, newPath] of Object.entries(config.pathMappings)) {
      // 如果文件已经包含新路径，跳过处理
      if (content.includes(newPath)) {
        continue;
      }
      
      content = content.replace(new RegExp(escapeRegExp(oldPath), 'g'), newPath);
    }
    
    // 如果内容有变化，写回文件
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`已修复: ${path.relative(process.cwd(), filePath)}`);
    }
  } catch (error) {
    console.error(`处理文件时出错 ${filePath}:`, error.message);
  }
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function main() {
  const buildPath = path.resolve(config.buildDir);
  
  if (!fs.existsSync(buildPath)) {
    console.error(`构建目录不存在: ${buildPath}`);
    console.error('请先运行构建命令生成构建产物');
    process.exit(1);
  }
  
  console.log(`🔧 修复静态资源路径...`);
  console.log(`📁 构建目录: ${buildPath}`);
  
  for (const [oldPath, newPath] of Object.entries(config.pathMappings)) {
    console.log(`📝 ${oldPath} → ${newPath}`);
  }
  
  processDirectory(buildPath);
  console.log(`✅ 完成！现在可以上传 ${config.buildDir} 到你的服务器`);
}

if (require.main === module) {
  main();
}