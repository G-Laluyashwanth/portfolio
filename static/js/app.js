/* =============================================================
   Portfolio — App JS
   Theme toggle · Mobile menu · Scroll reveal · Typing animation
   ============================================================= */

(() => {
  const root = document.body;
  const themeToggle = document.getElementById('theme-toggle');
  const navToggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.menu');

  /* ---------- Theme ---------- */
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const stored = localStorage.getItem('theme');

  const applyTheme = (theme) => {
    const isDark = theme === 'dark';
    root.classList.toggle('dark', isDark);
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', String(isDark));
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    }
  };

  applyTheme(stored || (prefersDark ? 'dark' : 'light'));

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const next = root.classList.contains('dark') ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('theme', next);
    });
  }

  /* ---------- Mobile menu ---------- */
  if (navToggle && menu) {
    navToggle.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    menu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        menu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');

  if (!reducedMotion && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14, rootMargin: '0px 0px -40px 0px' }
    );
    revealItems.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 70, 280)}ms`;
      io.observe(el);
    });
  } else {
    revealItems.forEach((el) => el.classList.add('is-visible'));
  }

  /* ---------- Typing animation ---------- */
  const typingTarget = document.getElementById('typing-target');
  const typingData = document.getElementById('typing-phrases');
  if (typingTarget && typingData && !reducedMotion) {
    let phrases = [];
    try { phrases = JSON.parse(typingData.textContent); } catch (e) { phrases = []; }
    if (phrases.length) {
      let pIdx = 0, cIdx = 0, deleting = false;
      const tick = () => {
        const current = phrases[pIdx];
        if (!deleting) {
          cIdx++;
          typingTarget.textContent = current.slice(0, cIdx);
          if (cIdx === current.length) {
            deleting = true;
            setTimeout(tick, 1600);
            return;
          }
          setTimeout(tick, 70);
        } else {
          cIdx--;
          typingTarget.textContent = current.slice(0, cIdx);
          if (cIdx === 0) {
            deleting = false;
            pIdx = (pIdx + 1) % phrases.length;
          }
          setTimeout(tick, 35);
        }
      };
      tick();
    }
  }
  /* ---------- Skills tab filter ---------- */
  const skillTabs = document.querySelectorAll('.skills-tab');
  const skillChips = document.querySelectorAll('.skill-chip');

  if (skillTabs.length) {
    // Show only the first category on load
    const firstFilter = skillTabs[0].dataset.filter;
    skillChips.forEach((chip) => {
      chip.classList.toggle('is-hidden', chip.dataset.category !== firstFilter);
    });

    skillTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        skillTabs.forEach((t) => {
          t.classList.remove('is-active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('is-active');
        tab.setAttribute('aria-selected', 'true');

        const filter = tab.dataset.filter;
        skillChips.forEach((chip) => {
          chip.classList.toggle('is-hidden', chip.dataset.category !== filter);
        });
      });
    });
  }
})();
