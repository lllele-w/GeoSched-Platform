/**
 * GeoSched 智策平台 - 公共脚本
 */

// 侧边栏图片轮播
document.addEventListener('DOMContentLoaded', () => {
  const imgs = document.querySelectorAll('.siw-img');
  const dots = document.querySelectorAll('.siw-dot');
  if (!imgs.length) return;
  let cur = 0;
  const CAPTIONS = ['数字地球 · 全球网络', '多星组网 · 协同调度', '星地链路 · 任务覆盖'];

  function goTo(idx) {
    imgs[cur].classList.remove('active');
    dots[cur].classList.remove('active');
    cur = (idx + imgs.length) % imgs.length;
    imgs[cur].classList.add('active');
    dots[cur].classList.add('active');
    const cap = document.querySelector('.siw-caption');
    if (cap) cap.textContent = CAPTIONS[cur];
  }

  dots.forEach((dot, i) => dot.addEventListener('click', () => goTo(i)));
  setInterval(() => goTo(cur + 1), 3800);
});

(function () {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.getAttribute('href') === page) el.classList.add('active');
  });
})();

// ECharts 通用深色主题配置
const CHART_THEME = {
  backgroundColor: 'transparent',
  textStyle: { color: 'rgba(190,215,255,0.62)' }
};

const TOOLTIP_STYLE = {
  backgroundColor: 'rgba(6,16,36,0.95)',
  borderColor: 'rgba(50,130,240,0.3)',
  borderWidth: 1,
  textStyle: { color: '#e2eeff', fontSize: 12 },
  extraCssText: 'box-shadow: 0 4px 16px rgba(0,0,0,0.5);'
};

// 坐标轴公共配色
const AXIS_STYLE = {
  axisLabel: { color: 'rgba(190,215,255,0.55)', fontSize: 11 },
  axisLine:  { lineStyle: { color: 'rgba(50,130,240,0.2)' } },
  splitLine: { lineStyle: { color: 'rgba(50,130,240,0.1)', type: 'dashed' } }
};

// 数字动画计数器
function animateCount(el, target, decimals = 0, duration = 1200) {
  const start = performance.now();
  const step = (now) => {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    const val = eased * target;
    el.textContent = decimals > 0 ? val.toFixed(decimals) : Math.round(val).toLocaleString('zh-CN');
    if (p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// 页面加载后执行数字动画
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const dec    = parseInt(el.dataset.dec || '0');
    animateCount(el, target, dec);
  });
});

// resize 时刷新所有已初始化 ECharts 实例
window.addEventListener('resize', () => {
  if (window.__echartsInstances) {
    window.__echartsInstances.forEach(c => c.resize());
  }
});

// 注册 ECharts 实例以支持 resize
function regChart(chart) {
  window.__echartsInstances = window.__echartsInstances || [];
  window.__echartsInstances.push(chart);
  return chart;
}
