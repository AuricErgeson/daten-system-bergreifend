'use strict';
const fs = require('fs');
const path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const svgDir = path.join(__dirname, 'screenshots');
const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg'));

for (const file of files) {
  const svgPath = path.join(svgDir, file);
  const pngPath = svgPath.replace('.svg', '.png');
  const svgContent = fs.readFileSync(svgPath);
  const resvg = new Resvg(svgContent, { fitTo: { mode: 'width', value: 1200 } });
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  fs.writeFileSync(pngPath, pngBuffer);
  console.log(`PNG: ${path.basename(pngPath)}  (${Math.round(pngBuffer.length / 1024)}KB)`);
}
