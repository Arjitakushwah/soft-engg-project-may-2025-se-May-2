// badge-svgs.js

// --- Base SVG Icons and Colors ---
const colors = {
    bronze: "#d08c4a",
    silver: "#c0c0c0",
    gold: "#ffd700",
    platinum: "#79c1f1",
    diamond: "#8b5cf6",
  };
  
  // ✨ NEW, MORE DETAILED ICON PATHS ✨
  const iconPaths = {
    streak: "M7.05 10.95L5.64 9.54L12 3l6.36 6.36l-1.41 1.41L12 5.83z M12 21l-6.36-6.36l1.41-1.41L12 18.17l4.95-4.95l1.41 1.41z", // A more abstract "spark" or "star"
    journal: "M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm-1 9V3.5L18.5 9H13zm4 9H7v-2h10v2zm0-4H7v-2h10v2zm-3-4H7V9h7v2z", // A document icon
    story: "M20 2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM9 18H7v-2h2v2zm0-4H7v-2h2v2zm0-4H7V8h2v2zm11 8h-8v-2h8v2zm0-4h-8v-2h8v2zm0-4h-8V8h8v2z", // A book with chapters
    infotainment: "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v2h-2V7zm0 4h2v6h-2v-6z" // A classic "info" icon
  };
  
  // --- SVG Generation Function ---
  function createBadge(iconPath, color, text) {
    return `
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 1.25l-10 4.25v6a10 10 0 0010 11.25 10 10 0 0010-11.25v-6l-10-4.25z" style="fill:${color}; stroke:#fff; stroke-width:1.5px;" />
        <path transform="scale(0.65) translate(6, 6)" d="${iconPath}" style="fill:#fff;" />
        ${text ? `<text x="12" y="19.5" font-size="5.5" fill="#fff" font-family="Arial, sans-serif" font-weight="bold" text-anchor="middle">${text}</text>` : ''}
      </svg>`;
  }
  
  // --- Badge to SVG Mapping (Uses new icons) ---
  export const badgeSvgMap = {
    'Streak 1 days': createBadge(iconPaths.streak, colors.bronze, '1'),
    'Streak 5 days': createBadge(iconPaths.streak, colors.bronze, '5'),
    'Streak 10 days': createBadge(iconPaths.streak, colors.silver, '10'),
    'Streak 15 days': createBadge(iconPaths.streak, colors.silver, '15'),
    'Streak 30 days': createBadge(iconPaths.streak, colors.gold, '30'),
    'Streak 50 days': createBadge(iconPaths.streak, colors.gold, '50'),
    'Streak 100 days': createBadge(iconPaths.streak, colors.platinum, '100'),
    'Journal x1': createBadge(iconPaths.journal, colors.bronze, '1'),
    'Journal x5': createBadge(iconPaths.journal, colors.bronze, '5'),
    'Journal x10': createBadge(iconPaths.journal, colors.silver, '10'),
    'Journal x20': createBadge(iconPaths.journal, colors.silver, '20'),
    'Journal x50': createBadge(iconPaths.journal, colors.gold, '50'),
    'Story x1': createBadge(iconPaths.story, colors.bronze, '1'),
    'Story x5': createBadge(iconPaths.story, colors.bronze, '5'),
    'Story x10': createBadge(iconPaths.story, colors.silver, '10'),
    'Story x20': createBadge(iconPaths.story, colors.silver, '20'),
    'Story x50': createBadge(iconPaths.story, colors.gold, '50'),
    'Infotainment x1': createBadge(iconPaths.infotainment, colors.bronze, '1'),
    'Infotainment x5': createBadge(iconPaths.infotainment, colors.bronze, '5'),
    'Infotainment x10': createBadge(iconPaths.infotainment, colors.silver, '10'),
    'Infotainment x20': createBadge(iconPaths.infotainment, colors.silver, '20'),
    'Infotainment x50': createBadge(iconPaths.infotainment, colors.gold, '50'),
  };
  
  export const defaultBadgeSvg = createBadge("M12 6l-1.4 1.4 2.6 2.6H8v2h5.2l-2.6 2.6L12 16l5-5-5-5z", "#cccccc");