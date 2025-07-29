// 加载组件函数
function loadComponent(id, url) {
  fetch(url)
    .then((response) => response.text())
    .then((data) => {
      document.getElementById(id).innerHTML = data;
    })
    .catch((error) => {
      console.error("Error loading component:", error);
    });
}

// 增强卡片悬停效果，考虑动态加载的元素
function setupCardHoverEffects() {
  // 使用事件委托，在document上监听事件
  document.addEventListener("mousemove", (e) => {
    const card = e.target.closest(".card");
    if (!card) return;

    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    // 限制最大倾斜角度为15度
    const angleY = Math.min(Math.max((x - centerX) / 25, -15), 15);
    const angleX = Math.min(Math.max((centerY - y) / 25, -15), 15);

    card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateZ(10px)`;
  });

  // 鼠标离开卡片时重置效果
  document.addEventListener("mouseout", (e) => {
    // 检查是否真正离开了卡片
    if (
      !e.relatedTarget ||
      !e.target.closest(".card").contains(e.relatedTarget)
    ) {
      const card = e.target.closest(".card");
      if (card) {
        card.style.transform =
          "perspective(1000px) rotateX(0) rotateY(0) translateZ(0)";
      }
    }
  });
}

// 加载所有组件
document.addEventListener("DOMContentLoaded", function () {
  loadComponent("header", "components/header.html");
  loadComponent("hero", "components/hero.html");
  loadComponent("education", "components/education.html");
  loadComponent("projects", "components/projects.html");
  loadComponent("contact", "components/contact.html");
  loadComponent("footer", "components/footer.html");

  // 简单的滚动动画
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });

  // 初始设置卡片效果
  setupCardHoverEffects();

  // 使用setTimeout确保所有组件加载完成后再设置一次效果
  setTimeout(() => {
    setupCardHoverEffects();
  }, 1000);
});
