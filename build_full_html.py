# -*- coding: utf-8 -*-
"""
Full HTML Assembler for LexiUp
"""
import json
import os

from build_lexiup import VOCAB_ITEMS
from generate_app import EXTENDED_ITEMS

vocab_json = json.dumps(VOCAB_ITEMS, ensure_ascii=False)
extended_json = json.dumps(EXTENDED_ITEMS, ensure_ascii=False)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="vi" data-theme="light" data-font="md">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <title>LexiUp - Học Từ Vựng Tiếng Anh B1, B2, C1 Thông Minh</title>
  <meta name="description" content="Ứng dụng học từ vựng tiếng Anh tương tác chuẩn CEFR B1, B2, C1 theo phương pháp lặp lại ngắt quãng (SRS) Memrise dành cho người Việt.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* ==========================================================================
       CSS VARIABLES & THEME SYSTEM (WCAG AA Compliant)
       ========================================================================== */
    :root {
      --primary: #0D9488;
      --primary-hover: #0F766E;
      --primary-active: #115E59;
      --primary-light: #E6FFFA;
      --primary-border: #99F6E4;
      --primary-glow: rgba(13, 148, 136, 0.25);

      --accent-amber: #D97706;
      --accent-amber-light: #FEF3C7;
      --accent-rose: #DC2626;
      --accent-rose-light: #FEE2E2;
      --accent-green: #059669;
      --accent-green-light: #D1FAE5;
      --accent-blue: #2563EB;
      --accent-blue-light: #DBEAFE;
      --accent-purple: #7C3AED;
      --accent-purple-light: #EDE9FE;

      --bg-body: #F8FAFC;
      --bg-card: #FFFFFF;
      --bg-subtle: #F1F5F9;
      --bg-input: #FFFFFF;
      --border-color: #E2E8F0;
      --border-focus: #0D9488;

      --text-main: #0F172A;
      --text-muted: #475569;
      --text-sub: #64748B;
      --text-inverse: #FFFFFF;

      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 26px;
      --radius-full: 9999px;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);

      --font-scale: 16px;
      --trans-fast: 0.15s ease;
      --trans-normal: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    [data-theme="dark"] {
      --primary: #14B8A6;
      --primary-hover: #2DD4BF;
      --primary-active: #5EEAD4;
      --primary-light: rgba(20, 184, 166, 0.15);
      --primary-border: #134E4A;
      --primary-glow: rgba(20, 184, 166, 0.35);

      --accent-amber: #FBBF24;
      --accent-amber-light: rgba(245, 158, 11, 0.18);
      --accent-rose: #F87171;
      --accent-rose-light: rgba(239, 68, 68, 0.18);
      --accent-green: #34D399;
      --accent-green-light: rgba(16, 185, 129, 0.18);
      --accent-blue: #60A5FA;
      --accent-blue-light: rgba(59, 130, 246, 0.18);
      --accent-purple: #A78BFA;
      --accent-purple-light: rgba(139, 92, 246, 0.18);

      --bg-body: #0F172A;
      --bg-card: #1E293B;
      --bg-subtle: #334155;
      --bg-input: #1E293B;
      --border-color: #334155;
      --border-focus: #14B8A6;

      --text-main: #F8FAFC;
      --text-muted: #CBD5E1;
      --text-sub: #94A3B8;
      --text-inverse: #0F172A;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }

    [data-font="sm"] { --font-scale: 14px; }
    [data-font="md"] { --font-scale: 16px; }
    [data-font="lg"] { --font-scale: 18px; }

    /* ==========================================================================
       RESET & BASE STYLES
       ========================================================================== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html {
      font-size: var(--font-scale);
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-body);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.5;
      transition: background-color var(--trans-normal), color var(--trans-normal);
    }

    button, input, select, textarea {
      font-family: inherit;
      font-size: inherit;
      color: inherit;
    }

    button {
      cursor: pointer;
      border: none;
      background: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: var(--trans-normal);
    }

    button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible {
      outline: 2px solid var(--border-focus);
      outline-offset: 2px;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    /* ==========================================================================
       LAYOUT & RESPONSIVE ARCHITECTURE
       ========================================================================== */
    .app-layout {
      display: flex;
      width: 100%;
      min-height: 100vh;
    }

    /* Desktop Sidebar */
    .desktop-sidebar {
      display: none;
      width: 260px;
      background: var(--bg-card);
      border-right: 1px solid var(--border-color);
      flex-direction: column;
      padding: 24px 16px;
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      z-index: 40;
    }

    .brand-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 12px;
      margin-bottom: 24px;
    }

    .brand-icon {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #0D9488, #2563EB);
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
    }

    .brand-title {
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: linear-gradient(135deg, var(--text-main), var(--primary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-sub);
    }

    .nav-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex: 1;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 16px;
      border-radius: var(--radius-md);
      font-weight: 600;
      font-size: 0.95rem;
      color: var(--text-muted);
      transition: var(--trans-fast);
      width: 100%;
      text-align: left;
    }

    .nav-link:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    .nav-link.active {
      background: var(--primary-light);
      color: var(--primary);
    }

    .nav-icon {
      font-size: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 24px;
    }

    /* Main Container */
    .main-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      padding-bottom: 80px; /* Space for mobile nav */
    }

    @media (min-width: 768px) {
      .desktop-sidebar {
        display: flex;
      }
      .main-wrapper {
        margin-left: 260px;
        padding-bottom: 40px;
      }
    }

    .top-header-mobile {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 18px;
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 30;
    }

    @media (min-width: 768px) {
      .top-header-mobile {
        display: none;
      }
    }

    .mobile-nav-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: var(--bg-card);
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-around;
      z-index: 40;
      padding-bottom: env(safe-area-inset-bottom);
    }

    @media (min-width: 768px) {
      .mobile-nav-bar {
        display: none;
      }
    }

    .mobile-nav-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      padding: 8px 12px;
      color: var(--text-sub);
      font-size: 0.72rem;
      font-weight: 600;
      min-width: 60px;
      min-height: 48px;
    }

    .mobile-nav-item.active {
      color: var(--primary);
    }

    .content-container {
      width: 100%;
      max-width: 1040px;
      margin: 0 auto;
      padding: 20px 16px;
    }

    @media (min-width: 768px) {
      .content-container {
        padding: 32px 28px;
      }
    }

    /* Screen Views */
    .view-screen {
      display: none;
      animation: fadeIn 0.3s ease-out;
    }

    .view-screen.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ==========================================================================
       DASHBOARD COMPONENTS
       ========================================================================== */
    .hero-greeting-bar {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 24px;
    }

    .greeting-title {
      font-size: 1.6rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: var(--text-main);
    }

    .greeting-subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
    }

    .gamification-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }

    .stat-pill {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 16px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: var(--shadow-sm);
    }

    .stat-pill-icon {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }

    .stat-pill-streak { background: var(--accent-amber-light); color: var(--accent-amber); }
    .stat-pill-xp { background: var(--accent-blue-light); color: var(--accent-blue); }
    .stat-pill-goal { background: var(--primary-light); color: var(--primary); }

    .stat-pill-meta {
      display: flex;
      flex-direction: column;
      min-width: 0;
    }

    .stat-pill-value {
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .stat-pill-label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-sub);
    }

    /* Hero CTA Cards */
    .cta-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      margin-bottom: 28px;
    }

    @media (min-width: 640px) {
      .cta-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    .hero-action-card {
      background: var(--bg-card);
      border: 2px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
      transition: transform var(--trans-fast), box-shadow var(--trans-fast), border-color var(--trans-fast);
    }

    .hero-action-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
    }

    .hero-card-learn {
      border-color: var(--primary-border);
      background: linear-gradient(145deg, var(--bg-card), var(--primary-light));
    }

    .hero-card-review {
      border-color: var(--accent-amber);
      background: linear-gradient(145deg, var(--bg-card), var(--accent-amber-light));
    }

    .card-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-size: 0.75rem;
      font-weight: 700;
      width: fit-content;
    }

    .btn-main-cta {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      min-height: 50px;
      border-radius: var(--radius-md);
      font-weight: 700;
      font-size: 1rem;
      box-shadow: var(--shadow-sm);
      transition: var(--trans-normal);
    }

    .btn-primary-gradient {
      background: linear-gradient(135deg, #0D9488, #059669);
      color: #FFFFFF;
    }

    .btn-primary-gradient:hover {
      background: linear-gradient(135deg, #0F766E, #047857);
      box-shadow: var(--shadow-md);
    }

    .btn-amber-gradient {
      background: linear-gradient(135deg, #D97706, #B45309);
      color: #FFFFFF;
    }

    .btn-amber-gradient:hover {
      background: linear-gradient(135deg, #B45309, #92400E);
      box-shadow: var(--shadow-md);
    }

    /* Quick Level Jump Cards */
    .section-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }

    .section-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .level-quick-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
      margin-bottom: 28px;
    }

    @media (min-width: 640px) {
      .level-quick-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }

    .level-pill-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 16px;
      cursor: pointer;
      transition: var(--trans-fast);
      display: flex;
      flex-direction: column;
      gap: 12px;
      box-shadow: var(--shadow-sm);
    }

    .level-pill-card:hover {
      border-color: var(--primary);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .level-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      width: fit-content;
    }

    .badge-b1 { background: var(--accent-green-light); color: var(--accent-green); }
    .badge-b2 { background: var(--accent-blue-light); color: var(--accent-blue); }
    .badge-c1 { background: var(--accent-purple-light); color: var(--accent-purple); }

    .progress-bar-bg {
      width: 100%;
      height: 8px;
      background: var(--bg-subtle);
      border-radius: var(--radius-full);
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      background: var(--primary);
      border-radius: var(--radius-full);
      transition: width 0.5s ease;
    }

    /* Daily Quote Card */
    .tip-card {
      background: var(--bg-card);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }

    .tip-icon {
      font-size: 24px;
      flex-shrink: 0;
    }

    /* ==========================================================================
       COURSE LIBRARY VIEW
       ========================================================================== */
    .search-bar-wrap {
      position: relative;
      margin-bottom: 20px;
    }

    .search-input {
      width: 100%;
      height: 48px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      padding: 0 44px 0 46px;
      font-size: 0.95rem;
      box-shadow: var(--shadow-sm);
      transition: var(--trans-fast);
    }

    .search-input:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    .search-icon-left {
      position: absolute;
      left: 18px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
      pointer-events: none;
      font-size: 1.1rem;
    }

    .search-clear-btn {
      position: absolute;
      right: 14px;
      top: 50%;
      transform: translateY(-50%);
      width: 28px;
      height: 28px;
      border-radius: var(--radius-full);
      color: var(--text-sub);
      font-size: 1.1rem;
      display: none;
    }

    .cefr-tabs {
      display: flex;
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 4px;
      gap: 4px;
      margin-bottom: 24px;
    }

    .cefr-tab-btn {
      flex: 1;
      padding: 10px 12px;
      border-radius: var(--radius-sm);
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--text-muted);
      transition: var(--trans-fast);
      text-align: center;
    }

    .cefr-tab-btn.active {
      background: var(--bg-card);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    .topic-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }

    @media (min-width: 640px) {
      .topic-grid {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    .topic-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: var(--shadow-sm);
      transition: var(--trans-fast);
    }

    .topic-card:hover {
      box-shadow: var(--shadow-md);
      border-color: var(--primary);
    }

    .topic-header {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .topic-icon-wrap {
      width: 46px;
      height: 46px;
      border-radius: var(--radius-md);
      background: var(--bg-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      flex-shrink: 0;
    }

    .topic-meta {
      flex: 1;
      min-width: 0;
    }

    .topic-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 2px;
    }

    .topic-actions {
      display: flex;
      gap: 10px;
      margin-top: 4px;
    }

    .btn-topic-learn {
      flex: 2;
      height: 40px;
      background: var(--primary);
      color: #FFFFFF;
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 0.85rem;
      gap: 6px;
    }

    .btn-topic-learn:hover {
      background: var(--primary-hover);
    }

    .btn-topic-view {
      flex: 1;
      height: 40px;
      background: var(--bg-subtle);
      color: var(--text-main);
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 0.85rem;
    }

    .btn-topic-view:hover {
      background: var(--border-color);
    }

    /* ==========================================================================
       SESSION VIEW (LEARNING / QUIZ ENGINE)
       ========================================================================== */
    .session-screen-wrapper {
      max-width: 640px;
      margin: 0 auto;
    }

    .session-topbar {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 20px;
    }

    .btn-exit-session {
      width: 40px;
      height: 40px;
      border-radius: var(--radius-full);
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 1.2rem;
      flex-shrink: 0;
    }

    .btn-exit-session:hover {
      background: var(--bg-subtle);
      color: var(--accent-rose);
    }

    .session-progress-wrap {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .session-progress-bar {
      width: 100%;
      height: 10px;
      background: var(--bg-subtle);
      border-radius: var(--radius-full);
      overflow: hidden;
    }

    .session-progress-inner {
      height: 100%;
      background: linear-gradient(90deg, var(--primary), var(--accent-blue));
      border-radius: var(--radius-full);
      transition: width 0.3s ease;
    }

    .session-meta-row {
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-sub);
    }

    /* 3D Flip Card Container */
    .flip-card-container {
      perspective: 1000px;
      width: 100%;
      min-height: 400px;
      margin-bottom: 24px;
    }

    .flip-card-inner {
      position: relative;
      width: 100%;
      min-height: 400px;
      text-align: center;
      transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
      cursor: pointer;
    }

    .flip-card-inner.is-flipped {
      transform: rotateY(180deg);
    }

    .card-face {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: var(--radius-xl);
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: var(--shadow-lg);
      border: 2px solid var(--border-color);
      background: var(--bg-card);
    }

    .card-face-back {
      transform: rotateY(180deg);
      background: linear-gradient(160deg, var(--bg-card), var(--bg-subtle));
    }

    .flashcard-word-title {
      font-size: 2.2rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.5px;
      margin-bottom: 6px;
    }

    .flashcard-ipa {
      font-family: inherit;
      font-size: 1.15rem;
      color: var(--primary);
      font-weight: 600;
      margin-bottom: 12px;
    }

    .flashcard-audio-btn {
      width: 58px;
      height: 58px;
      border-radius: var(--radius-full);
      background: var(--primary-light);
      color: var(--primary);
      font-size: 24px;
      margin: 16px auto;
      box-shadow: var(--shadow-sm);
      transition: transform var(--trans-fast), background var(--trans-fast);
    }

    .flashcard-audio-btn:hover {
      transform: scale(1.08);
      background: var(--primary);
      color: #FFFFFF;
    }

    .flashcard-hint-text {
      font-size: 0.85rem;
      color: var(--text-sub);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .flashcard-meaning {
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 8px;
    }

    .flashcard-def-en {
      font-size: 0.92rem;
      color: var(--text-muted);
      margin-bottom: 16px;
      font-style: italic;
    }

    .flashcard-example-box {
      background: var(--bg-card);
      border: 1px dashed var(--border-color);
      border-radius: var(--radius-md);
      padding: 14px;
      text-align: left;
      font-size: 0.95rem;
      margin-bottom: 12px;
    }

    .flashcard-example-en {
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .flashcard-example-vi {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    /* Quiz Stage Container */
    .quiz-stage-container {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 24px 20px;
      box-shadow: var(--shadow-md);
      margin-bottom: 24px;
      animation: fadeIn 0.25s ease;
    }

    .quiz-stage-container.shake {
      animation: shakeAnimation 0.4s cubic-bezier(.36,.07,.19,.97) both;
    }

    @keyframes shakeAnimation {
      10%, 90% { transform: translate3d(-2px, 0, 0); }
      20%, 80% { transform: translate3d(4px, 0, 0); }
      30%, 50%, 70% { transform: translate3d(-6px, 0, 0); }
      40%, 60% { transform: translate3d(6px, 0, 0); }
    }

    .quiz-question-type-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-size: 0.75rem;
      font-weight: 700;
      background: var(--bg-subtle);
      color: var(--text-sub);
      margin-bottom: 12px;
    }

    .quiz-question-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 18px;
    }

    .quiz-prompt-target {
      color: var(--primary);
      font-weight: 800;
      font-size: 1.35rem;
      display: block;
      margin-top: 4px;
    }

    /* Option Grid for Multiple Choice */
    .options-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    .quiz-option-btn {
      width: 100%;
      min-height: 52px;
      padding: 12px 16px;
      background: var(--bg-card);
      border: 2px solid var(--border-color);
      border-radius: var(--radius-md);
      font-size: 0.95rem;
      font-weight: 600;
      text-align: left;
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--text-main);
      transition: var(--trans-fast);
      position: relative;
    }

    .quiz-option-btn:hover:not(:disabled) {
      border-color: var(--primary);
      background: var(--primary-light);
    }

    .quiz-option-key {
      width: 26px;
      height: 26px;
      border-radius: var(--radius-sm);
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-muted);
      flex-shrink: 0;
    }

    .quiz-option-btn.correct {
      border-color: var(--accent-green) !important;
      background: var(--accent-green-light) !important;
      color: var(--accent-green) !important;
    }

    .quiz-option-btn.incorrect {
      border-color: var(--accent-rose) !important;
      background: var(--accent-rose-light) !important;
      color: var(--accent-rose) !important;
    }

    /* Typing Exercise */
    .typing-box-wrap {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-top: 10px;
    }

    .typing-input {
      width: 100%;
      height: 54px;
      border: 2px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 0 16px;
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      background: var(--bg-input);
      color: var(--text-main);
    }

    .typing-input:focus {
      border-color: var(--primary);
      outline: none;
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    .typing-hint-letters {
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: 3px;
      color: var(--text-muted);
      font-family: monospace;
    }

    /* Matching Game */
    .matching-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 12px;
    }

    .match-col {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .match-card-btn {
      min-height: 56px;
      padding: 8px 10px;
      border-radius: var(--radius-md);
      border: 2px solid var(--border-color);
      background: var(--bg-card);
      font-size: 0.88rem;
      font-weight: 600;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: var(--trans-fast);
      cursor: pointer;
    }

    .match-card-btn:hover {
      border-color: var(--primary);
    }

    .match-card-btn.selected {
      border-color: var(--primary);
      background: var(--primary-light);
      color: var(--primary);
    }

    .match-card-btn.matched {
      border-color: var(--accent-green);
      background: var(--accent-green-light);
      color: var(--accent-green);
      cursor: default;
      pointer-events: none;
      opacity: 0.7;
    }

    /* Feedback Banner */
    .feedback-banner {
      border-radius: var(--radius-md);
      padding: 16px;
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 16px;
      animation: fadeIn 0.2s ease;
    }

    .feedback-banner.show-correct {
      display: flex;
      background: var(--accent-green-light);
      border: 1px solid var(--accent-green);
      color: var(--accent-green);
    }

    .feedback-banner.show-wrong {
      display: flex;
      background: var(--accent-rose-light);
      border: 1px solid var(--accent-rose);
      color: var(--accent-rose);
    }

    .feedback-meta {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .feedback-title {
      font-weight: 800;
      font-size: 1rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .feedback-answer-hint {
      font-size: 0.85rem;
      color: var(--text-main);
    }

    .btn-feedback-next {
      height: 42px;
      padding: 0 18px;
      border-radius: var(--radius-sm);
      font-weight: 700;
      font-size: 0.9rem;
      background: var(--primary);
      color: #FFFFFF;
      flex-shrink: 0;
    }

    /* ==========================================================================
       SUMMARY VIEW (POST-SESSION)
       ========================================================================== */
    .summary-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 32px 24px;
      text-align: center;
      box-shadow: var(--shadow-lg);
      margin-bottom: 24px;
    }

    .summary-trophy {
      font-size: 4rem;
      margin-bottom: 12px;
      animation: bounceTrophy 1s infinite alternate;
    }

    @keyframes bounceTrophy {
      from { transform: translateY(0); }
      to { transform: translateY(-8px); }
    }

    .summary-stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin: 24px 0;
    }

    .summary-stat-box {
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 14px 10px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .summary-stat-num {
      font-size: 1.4rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .summary-stat-label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-sub);
    }

    .mistakes-review-box {
      text-align: left;
      margin-top: 24px;
      border-top: 1px solid var(--border-color);
      padding-top: 20px;
    }

    .mistake-item-pill {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      margin-bottom: 8px;
    }

    /* ==========================================================================
       PROGRESS VIEW
       ========================================================================== */
    .progress-stats-hero {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }

    @media (min-width: 640px) {
      .progress-stats-hero {
        grid-template-columns: repeat(4, 1fr);
      }
    }

    .chart-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 24px;
    }

    .barchart-container {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      height: 160px;
      padding-top: 20px;
      gap: 8px;
    }

    .barchart-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      height: 100%;
      justify-content: flex-end;
    }

    .barchart-bar-bg {
      width: 100%;
      max-width: 32px;
      height: 100%;
      background: var(--bg-subtle);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: flex-end;
      overflow: hidden;
    }

    .barchart-bar-inner {
      width: 100%;
      background: var(--primary);
      border-radius: var(--radius-sm);
      transition: height 0.6s ease;
      min-height: 4px;
    }

    .barchart-label {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-sub);
    }

    .leitner-boxes-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-top: 14px;
    }

    .leitner-box-item {
      background: var(--bg-subtle);
      border-radius: var(--radius-md);
      padding: 12px 6px;
      text-align: center;
    }

    .leitner-box-count {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .leitner-box-name {
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--text-sub);
    }

    /* ==========================================================================
       SETTINGS VIEW
       ========================================================================== */
    .settings-group {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-xl);
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }

    .settings-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 0;
      border-bottom: 1px solid var(--border-color);
      gap: 16px;
    }

    .settings-row:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }

    .settings-label-meta {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .settings-label-title {
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--text-main);
    }

    .settings-label-desc {
      font-size: 0.8rem;
      color: var(--text-sub);
    }

    /* Toggle Switch */
    .switch {
      position: relative;
      display: inline-block;
      width: 48px;
      height: 26px;
      flex-shrink: 0;
    }

    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: var(--bg-subtle);
      border: 1px solid var(--border-color);
      transition: .3s;
      border-radius: 34px;
    }

    .slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
      box-shadow: var(--shadow-sm);
    }

    input:checked + .slider {
      background-color: var(--primary);
    }

    input:checked + .slider:before {
      transform: translateX(22px);
    }

    .btn-segmented-wrap {
      display: flex;
      background: var(--bg-subtle);
      border-radius: var(--radius-sm);
      padding: 3px;
      gap: 3px;
    }

    .btn-seg {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-muted);
    }

    .btn-seg.active {
      background: var(--bg-card);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    /* ==========================================================================
       MODALS & DIALOGS
       ========================================================================== */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
      animation: fadeIn 0.2s ease;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-box {
      background: var(--bg-card);
      border-radius: var(--radius-xl);
      max-width: 520px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 24px;
      box-shadow: var(--shadow-xl);
      border: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .modal-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .modal-close-btn {
      width: 32px;
      height: 32px;
      border-radius: var(--radius-full);
      font-size: 1.2rem;
      color: var(--text-sub);
    }

    .modal-close-btn:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    /* Confetti Canvas */
    #confetti-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 200;
    }

    /* Toast */
    #toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 150;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .toast-pill {
      background: var(--text-main);
      color: var(--bg-body);
      padding: 12px 18px;
      border-radius: var(--radius-full);
      font-size: 0.88rem;
      font-weight: 600;
      box-shadow: var(--shadow-lg);
      display: flex;
      align-items: center;
      gap: 8px;
      animation: slideInDown 0.3s ease;
    }

    @keyframes slideInDown {
      from { transform: translateY(-10px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
  </style>
</head>
<body>

  <!-- Confetti Canvas -->
  <canvas id="confetti-canvas"></canvas>

  <!-- Toast Notification Container -->
  <div id="toast-container" aria-live="polite"></div>

  <div class="app-layout">
    <!-- Desktop Left Sidebar -->
    <aside class="desktop-sidebar" aria-label="Menu chính">
      <div class="brand-logo">
        <div class="brand-icon">L</div>
        <div>
          <div class="brand-title">LexiUp</div>
          <div class="brand-subtitle">Memrise English B1-C1</div>
        </div>
      </div>

      <nav class="nav-list" role="tablist">
        <button class="nav-link active" data-view="home" role="tab" aria-selected="true">
          <span class="nav-icon">🏠</span>
          <span>Trang chủ</span>
        </button>
        <button class="nav-link" data-view="library" role="tab" aria-selected="false">
          <span class="nav-icon">📚</span>
          <span>Thư viện từ vựng</span>
        </button>
        <button class="nav-link" data-view="progress" role="tab" aria-selected="false">
          <span class="nav-icon">📊</span>
          <span>Tiến độ học</span>
        </button>
        <button class="nav-link" data-view="settings" role="tab" aria-selected="false">
          <span class="nav-icon">⚙️</span>
          <span>Cài đặt & Nguồn</span>
        </button>
      </nav>

      <div style="margin-top: auto; padding-top: 16px; border-top: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);">Giao diện tối</span>
        <label class="switch">
          <input type="checkbox" id="sidebar-dark-toggle" aria-label="Bật tắt chế độ tối">
          <span class="slider"></span>
        </label>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-wrapper">
      <!-- Mobile Top Header -->
      <header class="top-header-mobile">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div class="brand-icon" style="width: 34px; height: 34px; font-size: 16px;">L</div>
          <span style="font-weight: 800; font-size: 1.15rem; color: var(--text-main);">LexiUp</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="card-badge" style="background: var(--accent-amber-light); color: var(--accent-amber);">
            🔥 <span id="mobile-streak-val">0</span>
          </div>
          <div class="card-badge" style="background: var(--primary-light); color: var(--primary);">
            ⚡ <span id="mobile-xp-val">0</span>
          </div>
        </div>
      </header>

      <main class="content-container" id="main-content">

        <!-- ==========================================
             VIEW 1: TRANG CHỦ / DASHBOARD
             ========================================== -->
        <section id="view-home" class="view-screen active" role="tabpanel" aria-labelledby="tab-home">
          <div class="hero-greeting-bar">
            <h1 class="greeting-title" id="greeting-text">Chào bạn! 👋</h1>
            <p class="greeting-subtitle" id="current-date-text">Sẵn sàng nâng cấp vốn từ vựng hôm nay?</p>
          </div>

          <!-- Stats Strip -->
          <div class="gamification-strip">
            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-streak">🔥</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="dash-streak-count">0 ngày</span>
                <span class="stat-pill-label">Chuỗi ngày</span>
              </div>
            </div>

            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-xp">⚡</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="dash-xp-count">0 XP</span>
                <span class="stat-pill-label">Điểm tích lũy</span>
              </div>
            </div>

            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-goal">🎯</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="dash-goal-text">0 / 10 từ</span>
                <span class="stat-pill-label">Mục tiêu ngày</span>
              </div>
            </div>
          </div>

          <!-- Primary Hero Actions -->
          <div class="cta-grid">
            <div class="hero-action-card hero-card-learn">
              <div>
                <span class="card-badge" style="background: var(--primary-light); color: var(--primary); margin-bottom: 8px;">
                  🚀 Học từ mới
                </span>
                <h2 style="font-size: 1.3rem; font-weight: 800; margin-bottom: 6px;">Tiếp tục phiên học</h2>
                <p style="font-size: 0.88rem; color: var(--text-muted);" id="dash-next-topic-desc">
                  Bộ 10 từ tiếp theo được cá nhân hóa theo trình độ của bạn.
                </p>
              </div>
              <button class="btn-main-cta btn-primary-gradient" id="btn-start-continue-learn">
                <span>Học tiếp ngay</span>
                <span>👉</span>
              </button>
            </div>

            <div class="hero-action-card hero-card-review">
              <div>
                <span class="card-badge" style="background: var(--accent-amber-light); color: var(--accent-amber); margin-bottom: 8px;">
                  🔄 Lặp lại ngắt quãng (SRS)
                </span>
                <h2 style="font-size: 1.3rem; font-weight: 800; margin-bottom: 6px;">Ôn tập định kỳ</h2>
                <p style="font-size: 0.88rem; color: var(--text-muted);" id="dash-due-count-desc">
                  Đang kiểm tra từ đến hạn ôn...
                </p>
              </div>
              <button class="btn-main-cta btn-amber-gradient" id="btn-start-due-review">
                <span>Ôn tập ngay</span>
                <span id="btn-due-counter-badge">(0)</span>
              </button>
            </div>
          </div>

          <!-- Quick Jump CEFR Levels -->
          <div class="section-title-row">
            <h3 class="section-title">Khám phá theo cấp độ</h3>
            <button style="font-size: 0.85rem; font-weight: 700; color: var(--primary);" id="btn-go-library-all">
              Xem toàn bộ ➔
            </button>
          </div>

          <div class="level-quick-grid">
            <div class="level-pill-card" data-jump-level="B1">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="level-badge badge-b1">Cấp độ B1</span>
                <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);" id="b1-quick-ratio">0/30</span>
              </div>
              <div style="font-weight: 700; font-size: 1rem;">Trung cấp thiết yếu</div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="b1-quick-progress" style="width: 0%; background: var(--accent-green);"></div>
              </div>
            </div>

            <div class="level-pill-card" data-jump-level="B2">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="level-badge badge-b2">Cấp độ B2</span>
                <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);" id="b2-quick-ratio">0/30</span>
              </div>
              <div style="font-weight: 700; font-size: 1rem;">Trung cấp nâng cao</div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="b2-quick-progress" style="width: 0%; background: var(--accent-blue);"></div>
              </div>
            </div>

            <div class="level-pill-card" data-jump-level="C1">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="level-badge badge-c1">Cấp độ C1</span>
                <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);" id="c1-quick-ratio">0/30</span>
              </div>
              <div style="font-weight: 700; font-size: 1rem;">Học thuật & Tranh biện</div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" id="c1-quick-progress" style="width: 0%; background: var(--accent-purple);"></div>
              </div>
            </div>
          </div>

          <!-- Tip of the Day -->
          <div class="tip-card">
            <div class="tip-icon">💡</div>
            <div>
              <div style="font-weight: 800; font-size: 0.95rem; margin-bottom: 2px;">Phương pháp Leitner 5 Hộp</div>
              <div style="font-size: 0.85rem; color: var(--text-muted);">
                Từ trả lời đúng sẽ nhảy sang hộp có chu kỳ ôn xa hơn (1 ngày ➔ 3 ngày ➔ 7 ngày ➔ 14 ngày ➔ 30 ngày). Từ làm sai sẽ quay về Hộp 1 để củng cố ngay!
              </div>
            </div>
          </div>
        </section>

        <!-- ==========================================
             VIEW 2: THƯ VIỆN KHÓA HỌC / LIBRARY
             ========================================== -->
        <section id="view-library" class="view-screen" role="tabpanel" aria-labelledby="tab-library">
          <div class="section-title-row">
            <div>
              <h1 class="greeting-title">Thư viện từ vựng</h1>
              <p class="greeting-subtitle">Chọn cấp độ và chủ đề để luyện tập có định hướng.</p>
            </div>
          </div>

          <!-- Search Box -->
          <div class="search-bar-wrap">
            <span class="search-icon-left">🔍</span>
            <input type="text" id="library-search-input" class="search-input" placeholder="Tìm kiếm từ tiếng Anh, nghĩa tiếng Việt, chủ đề..." aria-label="Tìm kiếm từ vựng">
            <button id="search-clear-btn" class="search-clear-btn" aria-label="Xóa tìm kiếm">✕</button>
          </div>

          <!-- CEFR Level Tabs -->
          <div class="cefr-tabs" role="tablist">
            <button class="cefr-tab-btn active" data-cefr-tab="B1" role="tab" aria-selected="true">
              B1 - Trung cấp
            </button>
            <button class="cefr-tab-btn" data-cefr-tab="B2" role="tab" aria-selected="false">
              B2 - Nâng cao
            </button>
            <button class="cefr-tab-btn" data-cefr-tab="C1" role="tab" aria-selected="false">
              C1 - Thành thạo
            </button>
          </div>

          <!-- Topic Grid -->
          <div class="topic-grid" id="library-topic-grid">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- ==========================================
             VIEW 3: PHIÊN HỌC TƯƠNG TÁC (SESSION)
             ========================================== -->
        <section id="view-session" class="view-screen" role="region" aria-label="Phiên học bài tập">
          <div class="session-screen-wrapper">
            <!-- Session Top Bar -->
            <div class="session-topbar">
              <button class="btn-exit-session" id="btn-session-exit" aria-label="Thoát phiên học" title="Tạm dừng phiên học">
                ✕
              </button>
              <div class="session-progress-wrap">
                <div class="session-meta-row">
                  <span id="session-counter-text">Từ 1 / 10</span>
                  <span id="session-mode-badge" style="color: var(--primary);">Bộ từ mới</span>
                </div>
                <div class="session-progress-bar">
                  <div class="session-progress-inner" id="session-progress-fill" style="width: 10%;"></div>
                </div>
              </div>
            </div>

            <!-- Dynamic Session Stage Container -->
            <div id="session-stage-root">
              <!-- Rendered dynamically by Session Engine -->
            </div>
          </div>
        </section>

        <!-- ==========================================
             VIEW 4: TỔNG KẾT PHIÊN HỌC (SUMMARY)
             ========================================== -->
        <section id="view-summary" class="view-screen" role="region" aria-label="Tổng kết phiên học">
          <div class="session-screen-wrapper">
            <div class="summary-card">
              <div class="summary-trophy">🎉</div>
              <h1 style="font-size: 1.6rem; font-weight: 800; margin-bottom: 6px;">Hoàn thành xuất sắc!</h1>
              <p style="font-size: 0.92rem; color: var(--text-muted);">Bạn đã rèn luyện trí nhớ và tiến thêm một bước lớn!</p>

              <div class="summary-stats-grid">
                <div class="summary-stat-box">
                  <span class="summary-stat-num" id="sum-xp-earned" style="color: var(--primary);">+80</span>
                  <span class="summary-stat-label">XP nhận được</span>
                </div>
                <div class="summary-stat-box">
                  <span class="summary-stat-num" id="sum-accuracy-rate" style="color: var(--accent-green);">100%</span>
                  <span class="summary-stat-label">Độ chính xác</span>
                </div>
                <div class="summary-stat-box">
                  <span class="summary-stat-num" id="sum-words-count" style="color: var(--accent-blue);">10</span>
                  <span class="summary-stat-label">Từ đã ôn</span>
                </div>
              </div>

              <!-- Mistakes Review List -->
              <div class="mistakes-review-box" id="sum-mistakes-container" style="display: none;">
                <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 12px; color: var(--accent-rose);">
                  ⚠️ Từ cần chú ý củng cố lại:
                </div>
                <div id="sum-mistakes-list">
                  <!-- Rendered dynamically -->
                </div>
              </div>

              <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 24px;">
                <button class="btn-main-cta btn-primary-gradient" id="btn-summary-next-session">
                  <span>Học tiếp bộ mới</span>
                  <span>🚀</span>
                </button>
                <button class="btn-main-cta" id="btn-summary-home" style="background: var(--bg-subtle); color: var(--text-main);">
                  <span>Về trang chủ</span>
                  <span>🏠</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- ==========================================
             VIEW 5: TIẾN ĐỘ HỌC TẬP (PROGRESS)
             ========================================== -->
        <section id="view-progress" class="view-screen" role="tabpanel" aria-labelledby="tab-progress">
          <div class="section-title-row">
            <div>
              <h1 class="greeting-title">Tiến độ của bạn</h1>
              <p class="greeting-subtitle">Theo dõi sự tiến bộ và chu kỳ lặp lại ngắt quãng.</p>
            </div>
          </div>

          <!-- Hero Metrics -->
          <div class="progress-stats-hero">
            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-goal">📚</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="prog-total-learned">0</span>
                <span class="stat-pill-label">Tổng từ đã học</span>
              </div>
            </div>
            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-streak">🏆</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="prog-total-mastered">0</span>
                <span class="stat-pill-label">Từ thành thạo</span>
              </div>
            </div>
            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-streak">🔥</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="prog-streak-val">0 ngày</span>
                <span class="stat-pill-label">Chuỗi ngày</span>
              </div>
            </div>
            <div class="stat-pill">
              <div class="stat-pill-icon stat-pill-xp">⚡</div>
              <div class="stat-pill-meta">
                <span class="stat-pill-value" id="prog-xp-val">0 XP</span>
                <span class="stat-pill-label">Tổng XP</span>
              </div>
            </div>
          </div>

          <!-- 7-Day Activity Chart -->
          <div class="chart-card">
            <div class="section-title-row">
              <h3 class="section-title" style="font-size: 1.05rem;">Hoạt động 7 ngày gần nhất (XP)</h3>
              <span style="font-size: 0.8rem; color: var(--text-sub);">Cập nhật tự động</span>
            </div>
            <div class="barchart-container" id="seven-days-barchart">
              <!-- Rendered by JS -->
            </div>
          </div>

          <!-- Leitner 5-Box Distribution -->
          <div class="chart-card">
            <div class="section-title-row">
              <h3 class="section-title" style="font-size: 1.05rem;">Phân bố hộp ghi nhớ (Leitner SRS)</h3>
              <span style="font-size: 0.8rem; color: var(--text-sub);">5 Cấp độ trí nhớ</span>
            </div>
            <div class="leitner-boxes-row">
              <div class="leitner-box-item">
                <div class="leitner-box-count" id="box-count-1">0</div>
                <div class="leitner-box-name">Hộp 1<br>(1 ngày)</div>
              </div>
              <div class="leitner-box-item">
                <div class="leitner-box-count" id="box-count-2">0</div>
                <div class="leitner-box-name">Hộp 2<br>(3 ngày)</div>
              </div>
              <div class="leitner-box-item">
                <div class="leitner-box-count" id="box-count-3">0</div>
                <div class="leitner-box-name">Hộp 3<br>(7 ngày)</div>
              </div>
              <div class="leitner-box-item">
                <div class="leitner-box-count" id="box-count-4">0</div>
                <div class="leitner-box-name">Hộp 4<br>(14 ngày)</div>
              </div>
              <div class="leitner-box-item">
                <div class="leitner-box-count" id="box-count-5" style="color: var(--accent-green);">0</div>
                <div class="leitner-box-name">Hộp 5<br>(Thành thạo)</div>
              </div>
            </div>
          </div>
        </section>

        <!-- ==========================================
             VIEW 6: CÀI ĐẶT & QUẢN LÝ NGUỒN TỪ (SETTINGS)
             ========================================== -->
        <section id="view-settings" class="view-screen" role="tabpanel" aria-labelledby="tab-settings">
          <div class="section-title-row">
            <div>
              <h1 class="greeting-title">Cài đặt & Nguồn từ</h1>
              <p class="greeting-subtitle">Tùy biến trải nghiệm học và quản lý kho từ vựng.</p>
            </div>
          </div>

          <!-- Appearance & Accessibility -->
          <div class="settings-group">
            <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 12px; color: var(--text-main);">
              🎨 Giao diện & Trợ năng
            </h3>

            <div class="settings-row">
              <div class="settings-label-meta">
                <span class="settings-label-title">Chế độ tối (Dark Mode)</span>
                <span class="settings-label-desc">Giảm mỏi mắt khi học vào ban đêm</span>
              </div>
              <label class="switch">
                <input type="checkbox" id="settings-dark-toggle">
                <span class="slider"></span>
              </label>
            </div>

            <div class="settings-row">
              <div class="settings-label-meta">
                <span class="settings-label-title">Cỡ chữ hiển thị</span>
                <span class="settings-label-desc">Điều chỉnh độ lớn chữ toàn ứng dụng</span>
              </div>
              <div class="btn-segmented-wrap">
                <button class="btn-seg" data-font-btn="sm">Nhỏ</button>
                <button class="btn-seg active" data-font-btn="md">Vừa</button>
                <button class="btn-seg" data-font-btn="lg">Lớn</button>
              </div>
            </div>
          </div>

          <!-- Study Target & Sound -->
          <div class="settings-group">
            <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 12px; color: var(--text-main);">
              🎯 Mục tiêu & Âm thanh
            </h3>

            <div class="settings-row">
              <div class="settings-label-meta">
                <span class="settings-label-title">Mục tiêu từ mỗi ngày</span>
                <span class="settings-label-desc">Số lượng từ mới đặt mục tiêu hoàn thành</span>
              </div>
              <div class="btn-segmented-wrap">
                <button class="btn-seg" data-goal-btn="5">5</button>
                <button class="btn-seg active" data-goal-btn="10">10</button>
                <button class="btn-seg" data-goal-btn="15">15</button>
                <button class="btn-seg" data-goal-btn="20">20</button>
              </div>
            </div>

            <div class="settings-row">
              <div class="settings-label-meta">
                <span class="settings-label-title">Phát âm từ vựng (Web Speech API)</span>
                <span class="settings-label-desc">Tự động đọc giọng chuẩn en-US/en-GB</span>
              </div>
              <label class="switch">
                <input type="checkbox" id="settings-speech-toggle" checked>
                <span class="slider"></span>
              </label>
            </div>

            <div class="settings-row">
              <div class="settings-label-meta">
                <span class="settings-label-title">Hiệu ứng âm thanh</span>
                <span class="settings-label-desc">Âm thanh phản hồi khi trả lời đúng / sai</span>
              </div>
              <label class="switch">
                <input type="checkbox" id="settings-soundfx-toggle" checked>
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <!-- Vocabulary Management (JSON Source, Import/Export/Scale) -->
          <div class="settings-group">
            <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 6px; color: var(--text-main);">
              📦 Quản lý nguồn từ vựng
            </h3>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
              Hệ thống hỗ trợ nạp thêm 2000-3000 từ vựng theo cấu trúc JSON chuẩn CEFR.
            </p>

            <div style="background: var(--bg-subtle); border-radius: var(--radius-md); padding: 14px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-weight: 700; font-size: 0.95rem;">Kho từ vựng hiện tại:</div>
                <div style="font-size: 0.8rem; color: var(--text-sub);" id="settings-vocab-summary">
                  Đang tải...
                </div>
              </div>
              <span class="card-badge" style="background: var(--primary-light); color: var(--primary);" id="settings-vocab-total-badge">
                90 từ
              </span>
            </div>

            <div style="display: grid; grid-template-columns: 1fr; gap: 10px;">
              <button class="btn-main-cta" id="btn-open-import-modal" style="background: var(--primary); color: #FFFFFF; font-size: 0.92rem; min-height: 44px;">
                <span>📥 Nạp thêm từ vựng (Nhập JSON)</span>
              </button>

              <button class="btn-main-cta" id="btn-load-extended-pack" style="background: var(--accent-blue); color: #FFFFFF; font-size: 0.92rem; min-height: 44px;">
                <span>⚡ Nạp nhanh gói mở rộng 30+ từ Oxford B1-C1</span>
              </button>

              <button class="btn-main-cta" id="btn-export-vocab-json" style="background: var(--bg-subtle); color: var(--text-main); font-size: 0.92rem; min-height: 44px;">
                <span>📤 Xuất dữ liệu từ vựng (.JSON)</span>
              </button>

              <button class="btn-main-cta" id="btn-reset-progress-modal" style="background: var(--bg-subtle); color: var(--accent-amber); font-size: 0.92rem; min-height: 44px;">
                <span>🔄 Đặt lại tiến độ học (Giữ nguyên từ vựng)</span>
              </button>

              <button class="btn-main-cta" id="btn-factory-reset" style="background: var(--bg-subtle); color: var(--accent-rose); font-size: 0.92rem; min-height: 44px;">
                <span>⚠️ Khôi phục cài đặt gốc</span>
              </button>
            </div>
          </div>
        </section>

      </main>

      <!-- Mobile Bottom Nav Bar -->
      <nav class="mobile-nav-bar" aria-label="Thanh điều hướng di động">
        <button class="mobile-nav-item active" data-view="home" aria-label="Trang chủ">
          <span style="font-size: 1.25rem;">🏠</span>
          <span>Trang chủ</span>
        </button>
        <button class="mobile-nav-item" data-view="library" aria-label="Thư viện">
          <span style="font-size: 1.25rem;">📚</span>
          <span>Thư viện</span>
        </button>
        <button class="mobile-nav-item" data-view="progress" aria-label="Tiến độ">
          <span style="font-size: 1.25rem;">📊</span>
          <span>Tiến độ</span>
        </button>
        <button class="mobile-nav-item" data-view="settings" aria-label="Cài đặt">
          <span style="font-size: 1.25rem;">⚙️</span>
          <span>Cài đặt</span>
        </button>
      </nav>
    </div>
  </div>

  <!-- ==========================================
       MODALS
       ========================================== -->

  <!-- Modal 1: Topic Word Preview Modal -->
  <div class="modal-overlay" id="modal-topic-preview" role="dialog" aria-modal="true" aria-labelledby="topic-preview-title">
    <div class="modal-box">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span id="topic-preview-icon" style="font-size: 1.6rem;">✈️</span>
          <h2 class="modal-title" id="topic-preview-title">Danh sách từ</h2>
        </div>
        <button class="modal-close-btn" id="btn-close-topic-modal" aria-label="Đóng">✕</button>
      </div>

      <div style="font-size: 0.85rem; color: var(--text-muted);" id="topic-preview-meta">
        Cấp độ B1 • 8 từ vựng
      </div>

      <div id="topic-preview-words-list" style="display: flex; flex-direction: column; gap: 10px; max-height: 50vh; overflow-y: auto; padding-right: 4px;">
        <!-- Rendered dynamically -->
      </div>

      <div style="display: flex; gap: 10px; margin-top: 8px;">
        <button class="btn-main-cta btn-primary-gradient" id="btn-modal-start-this-topic" style="min-height: 46px;">
          <span>Học chủ đề này ngay</span>
          <span>👉</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Modal 2: Import JSON Vocabulary -->
  <div class="modal-overlay" id="modal-import-vocab" role="dialog" aria-modal="true" aria-labelledby="import-title">
    <div class="modal-box">
      <div class="modal-header">
        <h2 class="modal-title" id="import-title">📥 Nạp thêm từ vựng JSON</h2>
        <button class="modal-close-btn" id="btn-close-import-modal" aria-label="Đóng">✕</button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted);">
        Dán mảng JSON chứa các từ mới theo cấu trúc chuẩn:
        <code>{"word", "ipa", "pos", "meaningVi", "definitionEn", "example", "exampleVi", "level", "topic"}</code>
      </p>

      <textarea id="import-json-textarea" style="width: 100%; height: 160px; border-radius: var(--radius-md); border: 1px solid var(--border-color); background: var(--bg-subtle); padding: 12px; font-family: monospace; font-size: 0.82rem; resize: vertical;" placeholder='[\n  {\n    "word": "resilience",\n    "ipa": "/rɪˈzɪliəns/",\n    "pos": "noun",\n    "meaningVi": "sự kiên cường",\n    "definitionEn": "The capacity to recover quickly from difficulties.",\n    "example": "Psychological resilience enables individuals to overcome adversity.",\n    "exampleVi": "Sức bật tâm lý kiên cường giúp các cá nhân vượt qua nghịch cảnh.",\n    "level": "C1",\n    "topic": "Tâm lý & Nhận thức"\n  }\n]'></textarea>

      <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
        <label class="btn-main-cta" style="background: var(--bg-subtle); color: var(--text-main); font-size: 0.85rem; cursor: pointer; min-height: 40px; padding: 0 14px;">
          <span>📂 Chọn file .json</span>
          <input type="file" id="import-file-input" accept=".json" style="display: none;">
        </label>
        <button class="btn-main-cta btn-primary-gradient" id="btn-submit-import-json" style="min-height: 40px; padding: 0 18px; font-size: 0.85rem;">
          <span>Thêm vào kho từ</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Modal 3: Exit Session Confirmation -->
  <div class="modal-overlay" id="modal-confirm-exit" role="dialog" aria-modal="true" aria-labelledby="exit-confirm-title">
    <div class="modal-box" style="max-width: 420px; text-align: center;">
      <div style="font-size: 2.5rem; margin-bottom: 4px;">⏸️</div>
      <h2 class="modal-title" id="exit-confirm-title" style="margin-bottom: 6px;">Tạm dừng phiên học?</h2>
      <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 18px;">
        Các từ bạn đã trả lời đúng trong phiên này vẫn sẽ được ghi nhận và lưu lại.
      </p>
      <div style="display: flex; gap: 10px;">
        <button class="btn-main-cta" id="btn-cancel-exit-session" style="background: var(--bg-subtle); color: var(--text-main); flex: 1;">
          Học tiếp
        </button>
        <button class="btn-main-cta" id="btn-confirm-exit-session" style="background: var(--accent-rose); color: #FFFFFF; flex: 1;">
          Rời khỏi
        </button>
      </div>
    </div>
  </div>

  <!-- Modal 4: Reset Confirmation -->
  <div class="modal-overlay" id="modal-confirm-reset" role="dialog" aria-modal="true" aria-labelledby="reset-confirm-title">
    <div class="modal-box" style="max-width: 420px; text-align: center;">
      <div style="font-size: 2.5rem; margin-bottom: 4px;">⚠️</div>
      <h2 class="modal-title" id="reset-confirm-title" style="margin-bottom: 6px;">Xác nhận đặt lại?</h2>
      <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 18px;" id="reset-confirm-desc">
        Hành động này sẽ đưa các từ về trạng thái Mới và đặt lại chuỗi học tập.
      </p>
      <div style="display: flex; gap: 10px;">
        <button class="btn-main-cta" id="btn-cancel-reset" style="background: var(--bg-subtle); color: var(--text-main); flex: 1;">
          Hủy bỏ
        </button>
        <button class="btn-main-cta" id="btn-execute-reset" style="background: var(--accent-rose); color: #FFFFFF; flex: 1;">
          Đồng ý
        </button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       JAVASCRIPT ARCHITECTURE & LOGIC
       ========================================================================== -->
  <script>
    /**
     * =========================================================================
     * 1. VOCABULARY DATA INITIALIZATION (const VOCAB = [...])
     * 90 Curated words for CEFR B1, B2, C1 across 12 topics
     * =========================================================================
     */
    const VOCAB = __VOCAB_JSON__;

    const EXTENDED_PACK = __EXTENDED_JSON__;

    /**
     * =========================================================================
     * 2. STORAGE & STATE MANAGEMENT (wrapped in try/catch)
     * =========================================================================
     */
    const STORAGE_KEYS = {
      VOCAB: 'lexiup_vocab_data',
      USER: 'lexiup_user_state',
      PROGRESS: 'lexiup_word_progress',
      HISTORY: 'lexiup_study_history'
    };

    const StorageManager = {
      isAvailable() {
        try {
          const testKey = '__test__';
          localStorage.setItem(testKey, testKey);
          localStorage.removeItem(testKey);
          return true;
        } catch (e) {
          return false;
        }
      },

      get(key, defaultValue) {
        try {
          if (!this.isAvailable()) return defaultValue;
          const item = localStorage.getItem(key);
          return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
          console.warn(`[StorageManager] Failed to get ${key}:`, e);
          return defaultValue;
        }
      },

      set(key, value) {
        try {
          if (!this.isAvailable()) return false;
          localStorage.setItem(key, JSON.stringify(value));
          return true;
        } catch (e) {
          console.warn(`[StorageManager] Failed to set ${key}:`, e);
          return false;
        }
      },

      clear() {
        try {
          if (this.isAvailable()) {
            localStorage.removeItem(STORAGE_KEYS.VOCAB);
            localStorage.removeItem(STORAGE_KEYS.USER);
            localStorage.removeItem(STORAGE_KEYS.PROGRESS);
            localStorage.removeItem(STORAGE_KEYS.HISTORY);
          }
        } catch (e) {
          console.warn('[StorageManager] Clear error:', e);
        }
      }
    };

    // User State Model
    let AppState = {
      vocabList: [],
      user: {
        xp: 0,
        streak: 0,
        lastStudyDate: null,
        dailyGoal: 10,
        todayLearnedCount: 0,
        theme: 'light',
        fontSize: 'md',
        soundEffectsEnabled: true,
        speechEnabled: true
      },
      wordProgress: {}, // wordId -> { box: 0..5, nextReview: timestamp, lastReview: timestamp, correctStreak: 0 }
      history: [] // [{ date: 'YYYY-MM-DD', xp: 50, wordsCount: 10 }]
    };

    function initAppState() {
      // 1. Vocabulary list
      const savedVocab = StorageManager.get(STORAGE_KEYS.VOCAB, null);
      if (savedVocab && Array.isArray(savedVocab) && savedVocab.length > 0) {
        AppState.vocabList = savedVocab;
      } else {
        AppState.vocabList = [...VOCAB];
        StorageManager.set(STORAGE_KEYS.VOCAB, AppState.vocabList);
      }

      // 2. User profile & settings
      const savedUser = StorageManager.get(STORAGE_KEYS.USER, null);
      if (savedUser) {
        AppState.user = { ...AppState.user, ...savedUser };
      }

      // 3. Spaced Repetition progress
      const savedProgress = StorageManager.get(STORAGE_KEYS.PROGRESS, null);
      if (savedProgress && typeof savedProgress === 'object') {
        AppState.wordProgress = savedProgress;
      }

      // 4. Study History
      const savedHistory = StorageManager.get(STORAGE_KEYS.HISTORY, null);
      if (savedHistory && Array.isArray(savedHistory)) {
        AppState.history = savedHistory;
      }

      // Verify streak and daily reset
      checkDailyResetAndStreak();

      // Apply initial theme & font
      applyTheme(AppState.user.theme);
      applyFontSize(AppState.user.fontSize);
    }

    function saveState() {
      StorageManager.set(STORAGE_KEYS.VOCAB, AppState.vocabList);
      StorageManager.set(STORAGE_KEYS.USER, AppState.user);
      StorageManager.set(STORAGE_KEYS.PROGRESS, AppState.wordProgress);
      StorageManager.set(STORAGE_KEYS.HISTORY, AppState.history);
    }

    function checkDailyResetAndStreak() {
      const today = new Date().toISOString().slice(0, 10);
      const last = AppState.user.lastStudyDate;

      if (!last) {
        AppState.user.todayLearnedCount = 0;
      } else if (last !== today) {
        const lastDate = new Date(last);
        const currDate = new Date(today);
        const diffDays = Math.round((currDate - lastDate) / (1000 * 60 * 60 * 24));

        if (diffDays === 1) {
          // Consecutive day, keep streak
        } else if (diffDays > 1) {
          // Streak broken
          AppState.user.streak = 0;
        }
        AppState.user.todayLearnedCount = 0;
      }
    }

    function recordActivity(xpEarned, wordsLearnedCount) {
      const today = new Date().toISOString().slice(0, 10);

      // Update streak
      if (AppState.user.lastStudyDate !== today) {
        AppState.user.streak = (AppState.user.streak || 0) + 1;
        AppState.user.lastStudyDate = today;
      }

      AppState.user.xp = (AppState.user.xp || 0) + xpEarned;
      AppState.user.todayLearnedCount = (AppState.user.todayLearnedCount || 0) + wordsLearnedCount;

      // Update history
      let todayEntry = AppState.history.find(h => h.date === today);
      if (!todayEntry) {
        todayEntry = { date: today, xp: 0, wordsCount: 0 };
        AppState.history.push(todayEntry);
      }
      todayEntry.xp += xpEarned;
      todayEntry.wordsCount += wordsLearnedCount;

      // Keep last 30 days
      if (AppState.history.length > 30) {
        AppState.history = AppState.history.slice(-30);
      }

      saveState();
      renderDashboard();
      renderProgressView();
    }

    /**
     * =========================================================================
     * 3. AUDIO & SPEECH SYNTHESIS ENGINE
     * Web Speech API (en-US / en-GB) + Web Audio API synthesizer
     * =========================================================================
     */
    let audioCtx = null;

    function getAudioContext() {
      if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
          audioCtx = new AudioContextClass();
        }
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      return audioCtx;
    }

    const AudioManager = {
      speak(text) {
        if (!AppState.user.speechEnabled) return;
        if (!('speechSynthesis' in window)) return;

        try {
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = 'en-US';
          utterance.rate = 0.88;

          const voices = window.speechSynthesis.getVoices();
          const enVoice = voices.find(v => v.lang.startsWith('en-US') || v.lang.startsWith('en-GB') || v.name.includes('English'));
          if (enVoice) {
            utterance.voice = enVoice;
          }

          window.speechSynthesis.speak(utterance);
        } catch (e) {
          console.warn('[AudioManager] Speech error:', e);
        }
      },

      playCorrectSound() {
        if (!AppState.user.soundEffectsEnabled) return;
        try {
          const ctx = getAudioContext();
          if (!ctx) return;

          const now = ctx.currentTime;
          const osc1 = ctx.createOscillator();
          const osc2 = ctx.createOscillator();
          const gain = ctx.createGain();

          osc1.type = 'sine';
          osc1.frequency.setValueAtTime(523.25, now); // C5
          osc1.frequency.setValueAtTime(659.25, now + 0.12); // E5

          osc2.type = 'triangle';
          osc2.frequency.setValueAtTime(783.99, now + 0.12); // G5

          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

          osc1.connect(gain);
          osc2.connect(gain);
          gain.connect(ctx.destination);

          osc1.start(now);
          osc2.start(now + 0.12);
          osc1.stop(now + 0.35);
          osc2.stop(now + 0.35);
        } catch (e) {
          console.warn('[AudioManager] Tone error:', e);
        }
      },

      playErrorSound() {
        if (!AppState.user.soundEffectsEnabled) return;
        try {
          const ctx = getAudioContext();
          if (!ctx) return;

          const now = ctx.currentTime;
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();

          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(220, now); // A3
          osc.frequency.setValueAtTime(196, now + 0.1); // G3

          gain.gain.setValueAtTime(0.14, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);

          osc.connect(gain);
          gain.connect(ctx.destination);

          osc.start(now);
          osc.stop(now + 0.3);
        } catch (e) {
          console.warn('[AudioManager] Tone error:', e);
        }
      }
    };

    /**
     * =========================================================================
     * 4. SPACED REPETITION ENGINE (LEITNER 5-BOX SYSTEM)
     * =========================================================================
     */
    const LEITNER_INTERVALS_MS = {
      1: 1 * 24 * 60 * 60 * 1000,       // Box 1: 1 day
      2: 3 * 24 * 60 * 60 * 1000,       // Box 2: 3 days
      3: 7 * 24 * 60 * 60 * 1000,       // Box 3: 7 days
      4: 14 * 24 * 60 * 60 * 1000,      // Box 4: 14 days
      5: 30 * 24 * 60 * 60 * 1000       // Box 5: 30 days (Mastered)
    };

    const SRSEngine = {
      getWordProgress(wordId) {
        return AppState.wordProgress[wordId] || {
          box: 0,
          nextReview: 0,
          lastReview: 0,
          correctStreak: 0
        };
      },

      getStatus(wordId) {
        const prog = this.getWordProgress(wordId);
        if (prog.box === 0) return 'Mới';
        if (prog.box <= 2) return 'Đang học';
        if (prog.box <= 4) return 'Đã nhớ';
        return 'Thành thạo';
      },

      isDue(wordId) {
        const prog = this.getWordProgress(wordId);
        return prog.box > 0 && Date.now() >= prog.nextReview;
      },

      getDueWords() {
        return AppState.vocabList.filter(w => this.isDue(w.id));
      },

      getNewWords(limit = 10, filterFn = null) {
        let list = AppState.vocabList.filter(w => {
          const prog = this.getWordProgress(w.id);
          return prog.box === 0;
        });
        if (filterFn) list = list.filter(filterFn);
        return list.slice(0, limit);
      },

      getTopicWords(topicName) {
        return AppState.vocabList.filter(w => w.topic === topicName);
      },

      recordAnswer(wordId, isCorrect) {
        const current = this.getWordProgress(wordId);
        let newBox = current.box;

        if (isCorrect) {
          newBox = Math.min(5, Math.max(1, current.box + 1));
          const interval = LEITNER_INTERVALS_MS[newBox] || LEITNER_INTERVALS_MS[1];
          AppState.wordProgress[wordId] = {
            box: newBox,
            nextReview: Date.now() + interval,
            lastReview: Date.now(),
            correctStreak: (current.correctStreak || 0) + 1
          };
        } else {
          // Failure drops to box 1
          AppState.wordProgress[wordId] = {
            box: 1,
            nextReview: Date.now() + LEITNER_INTERVALS_MS[1],
            lastReview: Date.now(),
            correctStreak: 0
          };
        }
        saveState();
      }
    };

    /**
     * =========================================================================
     * 5. CANVAS CONFETTI MICRO-INTERACTION
     * Pure vanilla JS particle effect
     * =========================================================================
     */
    const Confetti = {
      canvas: null,
      ctx: null,
      particles: [],
      animId: null,

      init() {
        this.canvas = document.getElementById('confetti-canvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());
      },

      resize() {
        if (!this.canvas) return;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      },

      fire() {
        if (!this.canvas || !this.ctx) this.init();
        const colors = ['#0D9488', '#2563EB', '#F59E0B', '#10B981', '#EC4899', '#8B5CF6'];
        this.particles = [];

        for (let i = 0; i < 90; i++) {
          this.particles.push({
            x: this.canvas.width / 2 + (Math.random() - 0.5) * 200,
            y: this.canvas.height * 0.45,
            vx: (Math.random() - 0.5) * 12,
            vy: Math.random() * -12 - 4,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            rotSpeed: (Math.random() - 0.5) * 10,
            life: 1,
            decay: Math.random() * 0.015 + 0.008
          });
        }

        if (this.animId) cancelAnimationFrame(this.animId);
        this.loop();
      },

      loop() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        let aliveCount = 0;

        for (let p of this.particles) {
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.28; // gravity
          p.rotation += p.rotSpeed;
          p.life -= p.decay;

          if (p.life > 0) {
            aliveCount++;
            this.ctx.save();
            this.ctx.translate(p.x, p.y);
            this.ctx.rotate((p.rotation * Math.PI) / 180);
            this.ctx.globalAlpha = Math.max(0, p.life);
            this.ctx.fillStyle = p.color;
            this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.4);
            this.ctx.restore();
          }
        }

        if (aliveCount > 0) {
          this.animId = requestAnimationFrame(() => this.loop());
        } else {
          this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
      }
    };

    /**
     * =========================================================================
     * 6. SESSION CONTROLLER & INTERACTIVE QUIZ MODES
     * 5 Exercise Modes: Multiple Choice (EN & VI), Typing, Listening, Fill Blank, Matching
     * Immediate feedback + Retry Queue for Mistakes
     * =========================================================================
     */
    let SessionState = {
      active: false,
      mode: 'learn', // 'learn' | 'review' | 'topic'
      queue: [],     // array of word objects
      retryQueue: [],
      currentIndex: 0,
      totalCount: 0,
      correctFirstTry: 0,
      xpEarned: 0,
      mistakes: [],
      currentQuestion: null,
      isAnswered: false
    };

    const SessionEngine = {
      startSession(words, mode = 'learn') {
        if (!words || words.length === 0) {
          showToast('Không có từ nào để bắt đầu phiên học!');
          return;
        }

        // Shuffle words
        const shuffled = [...words].sort(() => 0.5 - Math.random());

        SessionState = {
          active: true,
          mode: mode,
          queue: shuffled,
          retryQueue: [],
          currentIndex: 0,
          totalCount: shuffled.length,
          correctFirstTry: 0,
          xpEarned: 0,
          mistakes: [],
          currentQuestion: null,
          isAnswered: false
        };

        switchView('session');
        this.renderCurrentCard();
      },

      renderCurrentCard() {
        const root = document.getElementById('session-stage-root');
        if (!root) return;

        // Check if finished
        if (SessionState.queue.length === 0) {
          if (SessionState.retryQueue.length > 0) {
            // Re-run words that were missed!
            SessionState.queue = [...SessionState.retryQueue];
            SessionState.retryQueue = [];
            showToast('🔄 Ôn lại các từ bạn đã trả lời chưa chính xác!');
          } else {
            this.finishSession();
            return;
          }
        }

        const currentWord = SessionState.queue[0];
        const prog = SRSEngine.getWordProgress(currentWord.id);
        const isNewWord = prog.box === 0 && !currentWord._hasBeenIntroduced;

        // Update progress bar
        const done = SessionState.currentIndex;
        const total = Math.max(done + SessionState.queue.length, SessionState.totalCount);
        const percent = Math.min(100, Math.round((done / total) * 100));

        document.getElementById('session-counter-text').textContent = `Từ ${done + 1} / ${total}`;
        document.getElementById('session-progress-fill').style.width = `${percent}%`;
        document.getElementById('session-mode-badge').textContent =
          SessionState.mode === 'review' ? 'Ôn tập SRS' : 'Học từ vựng';

        SessionState.isAnswered = false;

        if (isNewWord) {
          // Show 3D Flashcard Introduction
          currentWord._hasBeenIntroduced = true;
          this.renderFlashcardIntro(currentWord, root);
        } else {
          // Generate interactive quiz question
          this.renderQuizQuestion(currentWord, root);
        }
      },

      renderFlashcardIntro(word, root) {
        root.innerHTML = `
          <div class="flip-card-container" id="session-flip-container" aria-label="Thẻ ghi nhớ từ mới">
            <div class="flip-card-inner" id="session-flip-card">
              <!-- FRONT FACE -->
              <div class="card-face card-face-front">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span class="level-badge badge-${word.level.toLowerCase()}">${word.level}</span>
                  <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);">${word.topic}</span>
                </div>

                <div style="margin: auto 0;">
                  <h2 class="flashcard-word-title">${word.word}</h2>
                  <div class="flashcard-ipa">${word.ipa} • <span style="font-weight: 500; font-size: 0.95rem;">${word.pos}</span></div>
                  <button class="flashcard-audio-btn" id="btn-flashcard-audio" aria-label="Nghe phát âm">
                    🔊
                  </button>
                  <p class="flashcard-hint-text">
                    <span>💡 Nhấn vào thẻ hoặc phím [Space] để lật xem nghĩa</span>
                  </p>
                </div>

                <div style="color: var(--text-sub); font-size: 0.8rem; font-weight: 600;">
                  Thẻ giới thiệu từ mới
                </div>
              </div>

              <!-- BACK FACE -->
              <div class="card-face card-face-back">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span class="level-badge badge-${word.level.toLowerCase()}">${word.level}</span>
                  <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-sub);">${word.pos}</span>
                </div>

                <div style="margin: auto 0;">
                  <div class="flashcard-meaning">${word.meaningVi}</div>
                  <div class="flashcard-def-en">"${word.definitionEn}"</div>

                  <div class="flashcard-example-box">
                    <div class="flashcard-example-en">"${word.example}"</div>
                    <div class="flashcard-example-vi">${word.exampleVi}</div>
                  </div>
                </div>

                <div style="color: var(--text-sub); font-size: 0.8rem; font-weight: 600;">
                  Chạm để lật lại • Bấm nút bên dưới để bắt đầu bài tập
                </div>
              </div>
            </div>
          </div>

          <button class="btn-main-cta btn-primary-gradient" id="btn-flashcard-continue" style="min-height: 52px; font-size: 1.05rem;">
            <span>Tôi đã hiểu từ này, bắt đầu bài tập</span>
            <span>👉</span>
          </button>
        `;

        // Automatically pronounce new word
        setTimeout(() => AudioManager.speak(word.word), 300);

        const card = document.getElementById('session-flip-card');
        card.addEventListener('click', () => {
          card.classList.toggle('is-flipped');
        });

        const audioBtn = document.getElementById('btn-flashcard-audio');
        audioBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          AudioManager.speak(word.word);
        });

        const contBtn = document.getElementById('btn-flashcard-continue');
        contBtn.addEventListener('click', () => {
          this.renderQuizQuestion(word, root);
        });
      },

      renderQuizQuestion(word, root) {
        // Pick a question type: Multiple Choice (EN & VI), Typing, Listening, Fill Blank, Matching Pairs
        const types = ['mc_vi', 'mc_en', 'typing', 'listening', 'fill_blank', 'matching'];
        const qType = types[Math.floor(Math.random() * types.length)];

        SessionState.currentQuestion = {
          word: word,
          type: qType
        };

        if (qType === 'mc_vi') {
          this.renderMultipleChoiceVi(word, root);
        } else if (qType === 'mc_en') {
          this.renderMultipleChoiceEn(word, root);
        } else if (qType === 'typing') {
          this.renderTypingQuestion(word, root);
        } else if (qType === 'listening') {
          this.renderListeningQuestion(word, root);
        } else if (qType === 'fill_blank') {
          this.renderFillBlankQuestion(word, root);
        } else {
          this.renderMatchingQuestion(word, root);
        }
      },

      /* Quiz Type 1: Chọn nghĩa tiếng Việt */
      renderMultipleChoiceVi(word, root) {
        // Distractors
        const distractors = AppState.vocabList
          .filter(w => w.id !== word.id)
          .sort(() => 0.5 - Math.random())
          .slice(0, 3)
          .map(w => w.meaningVi);

        const options = [word.meaningVi, ...distractors].sort(() => 0.5 - Math.random());

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">🎯 Trắc nghiệm nghĩa từ</span>
            <div class="quiz-question-title">
              Từ tiếng Anh sau có nghĩa là gì?
              <span class="quiz-prompt-target">${word.word} <span style="font-size: 1rem; font-weight: 500; color: var(--text-sub);">${word.ipa}</span></span>
            </div>

            <div class="options-grid">
              ${options.map((opt, i) => `
                <button class="quiz-option-btn" data-answer="${encodeURIComponent(opt)}" data-correct="${opt === word.meaningVi}">
                  <span class="quiz-option-key">${i + 1}</span>
                  <span style="flex: 1;">${opt}</span>
                </button>
              `).join('')}
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        this.bindOptionButtons(word);
      },

      /* Quiz Type 2: Chọn từ tiếng Anh theo nghĩa tiếng Việt */
      renderMultipleChoiceEn(word, root) {
        const distractors = AppState.vocabList
          .filter(w => w.id !== word.id)
          .sort(() => 0.5 - Math.random())
          .slice(0, 3)
          .map(w => w.word);

        const options = [word.word, ...distractors].sort(() => 0.5 - Math.random());

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">🎯 Chọn từ tiếng Anh</span>
            <div class="quiz-question-title">
              Từ nào tương ứng với nghĩa:
              <span class="quiz-prompt-target">"${word.meaningVi}" <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-sub);">(${word.pos})</span></span>
            </div>

            <div class="options-grid">
              ${options.map((opt, i) => `
                <button class="quiz-option-btn" data-answer="${encodeURIComponent(opt)}" data-correct="${opt === word.word}">
                  <span class="quiz-option-key">${i + 1}</span>
                  <span style="flex: 1; font-weight: 700;">${opt}</span>
                </button>
              `).join('')}
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        this.bindOptionButtons(word);
      },

      /* Quiz Type 3: Nghe chọn từ */
      renderListeningQuestion(word, root) {
        const distractors = AppState.vocabList
          .filter(w => w.id !== word.id)
          .sort(() => 0.5 - Math.random())
          .slice(0, 3)
          .map(w => w.word);

        const options = [word.word, ...distractors].sort(() => 0.5 - Math.random());

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">🎧 Nghe và chọn từ</span>
            <div class="quiz-question-title" style="text-align: center;">
              Nghe phát âm và chọn từ chính xác:
            </div>

            <div style="text-align: center; margin: 16px 0;">
              <button class="flashcard-audio-btn" id="btn-quiz-listen-replay" aria-label="Nghe lại phát âm">
                🔊
              </button>
              <div style="font-size: 0.8rem; color: var(--text-sub); margin-top: 4px;">Bấm để nghe lại</div>
            </div>

            <div class="options-grid">
              ${options.map((opt, i) => `
                <button class="quiz-option-btn" data-answer="${encodeURIComponent(opt)}" data-correct="${opt === word.word}">
                  <span class="quiz-option-key">${i + 1}</span>
                  <span style="flex: 1; font-weight: 700;">${opt}</span>
                </button>
              `).join('')}
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        // Auto play speech
        setTimeout(() => AudioManager.speak(word.word), 250);

        document.getElementById('btn-quiz-listen-replay').addEventListener('click', () => {
          AudioManager.speak(word.word);
        });

        this.bindOptionButtons(word);
      },

      /* Quiz Type 4: Điền từ vào câu ví dụ */
      renderFillBlankQuestion(word, root) {
        // Replace target word in example with blank
        const regex = new RegExp(`\\\\b${word.word}\\\\b`, 'gi');
        let maskedExample = word.example.replace(regex, '________');
        if (!maskedExample.includes('________')) {
          // Fallback if conjugation differs
          const firstWord = word.word.split(' ')[0];
          maskedExample = word.example.replace(new RegExp(`\\\\b${firstWord}\\\\w*`, 'gi'), '________');
        }

        const distractors = AppState.vocabList
          .filter(w => w.id !== word.id && w.pos === word.pos)
          .sort(() => 0.5 - Math.random())
          .slice(0, 3)
          .map(w => w.word);

        // If not enough same pos, pick any
        while (distractors.length < 3) {
          const rand = AppState.vocabList[Math.floor(Math.random() * AppState.vocabList.length)].word;
          if (rand !== word.word && !distractors.includes(rand)) distractors.push(rand);
        }

        const options = [word.word, ...distractors].sort(() => 0.5 - Math.random());

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">📝 Điền từ vào câu</span>
            <div class="quiz-question-title">
              Chọn từ thích hợp điền vào chỗ trống:
            </div>

            <div class="flashcard-example-box" style="margin-bottom: 18px; font-size: 1rem;">
              <div class="flashcard-example-en" style="color: var(--primary); font-weight: 700; line-height: 1.6;">
                "${maskedExample}"
              </div>
              <div class="flashcard-example-vi" style="margin-top: 6px;">
                Dịch: ${word.exampleVi}
              </div>
            </div>

            <div class="options-grid">
              ${options.map((opt, i) => `
                <button class="quiz-option-btn" data-answer="${encodeURIComponent(opt)}" data-correct="${opt === word.word}">
                  <span class="quiz-option-key">${i + 1}</span>
                  <span style="flex: 1; font-weight: 700;">${opt}</span>
                </button>
              `).join('')}
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        this.bindOptionButtons(word);
      },

      /* Quiz Type 5: Gõ lại từ (Spelling) */
      renderTypingQuestion(word, root) {
        // Length hint (e.g., d _ _ _ _ _ _ _ _ _)
        const firstLetter = word.word.charAt(0);
        let hintLetters = firstLetter + ' ' + word.word.slice(1).split('').map(c => c === ' ' ? ' ' : '_').join(' ');

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">⌨️ Gõ lại từ tiếng Anh</span>
            <div class="quiz-question-title">
              Gõ từ tiếng Anh tương ứng với:
              <span class="quiz-prompt-target">"${word.meaningVi}" <span style="font-size: 0.95rem; font-weight: 500; color: var(--text-sub);">(${word.pos})</span></span>
            </div>

            <div class="typing-box-wrap">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="typing-hint-letters" id="typing-hint-display">${hintLetters}</span>
                <button id="btn-give-hint" style="font-size: 0.8rem; font-weight: 700; color: var(--primary);">
                  💡 Gợi ý thêm
                </button>
              </div>

              <input type="text" id="quiz-typing-input" class="typing-input" placeholder="Nhập từ tiếng Anh..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" autofocus>

              <button class="btn-main-cta btn-primary-gradient" id="btn-submit-typing" style="min-height: 48px;">
                <span>Kiểm tra đáp án</span>
                <span>➔</span>
              </button>
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        const input = document.getElementById('quiz-typing-input');
        input.focus();

        let hintLevel = 1;
        document.getElementById('btn-give-hint').addEventListener('click', () => {
          hintLevel++;
          const revealed = word.word.slice(0, hintLevel);
          const rest = word.word.slice(hintLevel).split('').map(c => c === ' ' ? ' ' : '_').join(' ');
          document.getElementById('typing-hint-display').textContent = (revealed + ' ' + rest).trim();
          input.focus();
        });

        const checkTyping = () => {
          if (SessionState.isAnswered) return;
          const userVal = input.value.trim().toLowerCase();
          const targetVal = word.word.trim().toLowerCase();
          const isCorrect = userVal === targetVal;
          this.handleAnswerResult(isCorrect, word, targetVal);
        };

        document.getElementById('btn-submit-typing').addEventListener('click', checkTyping);
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            checkTyping();
          }
        });
      },

      /* Quiz Type 6: Ghép cặp từ - nghĩa (Matching Pairs) */
      renderMatchingQuestion(word, root) {
        // Pick 3 additional words from vocabList
        const pool = AppState.vocabList.filter(w => w.id !== word.id).sort(() => 0.5 - Math.random()).slice(0, 3);
        const setWords = [word, ...pool].sort(() => 0.5 - Math.random());
        const enItems = [...setWords].sort(() => 0.5 - Math.random());
        const viItems = [...setWords].sort(() => 0.5 - Math.random());

        let selectedEn = null;
        let selectedVi = null;
        let matchedCount = 0;

        root.innerHTML = `
          <div class="quiz-stage-container" id="quiz-card-box">
            <span class="quiz-question-type-badge">🧩 Ghép cặp từ và nghĩa</span>
            <div class="quiz-question-title">
              Nối từ tiếng Anh với nghĩa tiếng Việt tương ứng:
            </div>

            <div class="matching-grid">
              <div class="match-col" id="match-en-col">
                ${enItems.map(item => `
                  <button class="match-card-btn" data-en-id="${item.id}" data-type="en">
                    <strong>${item.word}</strong>
                  </button>
                `).join('')}
              </div>
              <div class="match-col" id="match-vi-col">
                ${viItems.map(item => `
                  <button class="match-card-btn" data-vi-id="${item.id}" data-type="vi">
                    <span>${item.meaningVi}</span>
                  </button>
                `).join('')}
              </div>
            </div>

            <div class="feedback-banner" id="quiz-feedback-banner">
              <div class="feedback-meta">
                <span class="feedback-title" id="feedback-title"></span>
                <span class="feedback-answer-hint" id="feedback-hint"></span>
              </div>
              <button class="btn-feedback-next" id="btn-quiz-next">Tiếp tục ➔</button>
            </div>
          </div>
        `;

        const enBtns = root.querySelectorAll('[data-type="en"]');
        const viBtns = root.querySelectorAll('[data-type="vi"]');

        const checkPair = () => {
          if (!selectedEn || !selectedVi) return;
          const enId = selectedEn.dataset.enId;
          const viId = selectedVi.dataset.viId;

          if (enId === viId) {
            // Correct match
            AudioManager.playCorrectSound();
            selectedEn.classList.remove('selected');
            selectedVi.classList.remove('selected');
            selectedEn.classList.add('matched');
            selectedVi.classList.add('matched');
            matchedCount++;
            selectedEn = null;
            selectedVi = null;

            if (matchedCount === setWords.length) {
              this.handleAnswerResult(true, word, 'Đã ghép đúng tất cả các cặp!');
            }
          } else {
            // Mismatch
            AudioManager.playErrorSound();
            const btn1 = selectedEn;
            const btn2 = selectedVi;
            btn1.style.borderColor = 'var(--accent-rose)';
            btn2.style.borderColor = 'var(--accent-rose)';
            setTimeout(() => {
              btn1.classList.remove('selected');
              btn2.classList.remove('selected');
              btn1.style.borderColor = '';
              btn2.style.borderColor = '';
            }, 500);
            selectedEn = null;
            selectedVi = null;
          }
        };

        enBtns.forEach(btn => {
          btn.addEventListener('click', () => {
            if (btn.classList.contains('matched') || SessionState.isAnswered) return;
            enBtns.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedEn = btn;
            AudioManager.speak(btn.textContent.trim());
            checkPair();
          });
        });

        viBtns.forEach(btn => {
          btn.addEventListener('click', () => {
            if (btn.classList.contains('matched') || SessionState.isAnswered) return;
            viBtns.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            selectedVi = btn;
            checkPair();
          });
        });
      },

      bindOptionButtons(word) {
        const optionBtns = document.querySelectorAll('.quiz-option-btn');
        optionBtns.forEach(btn => {
          btn.addEventListener('click', () => {
            if (SessionState.isAnswered) return;
            const isCorrect = btn.dataset.correct === 'true';
            this.handleAnswerResult(isCorrect, word, word.meaningVi);
            if (isCorrect) {
              btn.classList.add('correct');
            } else {
              btn.classList.add('incorrect');
              // Highlight the correct one
              optionBtns.forEach(b => {
                if (b.dataset.correct === 'true') b.classList.add('correct');
              });
            }
          });
        });
      },

      handleAnswerResult(isCorrect, word, expectedDisplay) {
        SessionState.isAnswered = true;
        const box = document.getElementById('quiz-card-box');
        const banner = document.getElementById('quiz-feedback-banner');
        const title = document.getElementById('feedback-title');
        const hint = document.getElementById('feedback-hint');
        const nextBtn = document.getElementById('btn-quiz-next');

        if (isCorrect) {
          AudioManager.playCorrectSound();
          SessionState.xpEarned += 10;
          if (!word._hasMissedOnce) {
            SessionState.correctFirstTry++;
          }
          SRSEngine.recordAnswer(word.id, true);

          banner.className = 'feedback-banner show-correct';
          title.innerHTML = '✅ Tuyệt vời! Chính xác (+10 XP)';
          hint.textContent = `${word.word} (${word.ipa}): ${word.meaningVi}`;

          // Auto speak
          AudioManager.speak(word.word);

          // Advance to next after delay or on click
          nextBtn.onclick = () => this.advanceNextWord();
          setTimeout(() => {
            if (SessionState.active && SessionState.isAnswered) {
              this.advanceNextWord();
            }
          }, 1400);

        } else {
          AudioManager.playErrorSound();
          if (box) box.classList.add('shake');
          word._hasMissedOnce = true;

          // Re-queue word so user must get it right before ending!
          SessionState.retryQueue.push(word);
          if (!SessionState.mistakes.some(m => m.id === word.id)) {
            SessionState.mistakes.push(word);
          }
          SRSEngine.recordAnswer(word.id, false);

          banner.className = 'feedback-banner show-wrong';
          title.innerHTML = '❌ Chưa chính xác!';
          hint.textContent = `Đáp án đúng: "${word.word}" (${word.ipa}) ➔ ${word.meaningVi}`;

          AudioManager.speak(word.word);
          nextBtn.onclick = () => this.advanceNextWord();
        }
      },

      advanceNextWord() {
        // Remove current head of queue
        SessionState.queue.shift();
        SessionState.currentIndex++;
        this.renderCurrentCard();
      },

      finishSession() {
        SessionState.active = false;
        Confetti.fire();

        const totalItems = SessionState.totalCount;
        const accuracy = totalItems > 0 ? Math.round((SessionState.correctFirstTry / totalItems) * 100) : 100;

        // Record activity & XP
        recordActivity(SessionState.xpEarned, totalItems);

        // Populate summary screen
        document.getElementById('sum-xp-earned').textContent = `+${SessionState.xpEarned} XP`;
        document.getElementById('sum-accuracy-rate').textContent = `${accuracy}%`;
        document.getElementById('sum-words-count').textContent = `${totalItems}`;

        // Populate mistakes list if any
        const mistakesBox = document.getElementById('sum-mistakes-container');
        const mistakesList = document.getElementById('sum-mistakes-list');
        if (SessionState.mistakes.length > 0) {
          mistakesBox.style.display = 'block';
          mistakesList.innerHTML = SessionState.mistakes.map(m => `
            <div class="mistake-item-pill">
              <div>
                <strong style="color: var(--text-main); font-size: 0.95rem;">${m.word}</strong>
                <span style="color: var(--primary); font-size: 0.85rem; margin-left: 6px;">${m.ipa}</span>
                <div style="font-size: 0.82rem; color: var(--text-muted);">${m.meaningVi}</div>
              </div>
              <button class="flashcard-audio-btn" style="width: 36px; height: 36px; font-size: 16px; margin: 0;" onclick="AudioManager.speak('${m.word}')" aria-label="Nghe từ ${m.word}">
                🔊
              </button>
            </div>
          `).join('');
        } else {
          mistakesBox.style.display = 'none';
        }

        switchView('summary');
      }
    };

    /**
     * =========================================================================
     * 7. UI CONTROLLERS & VIEWS RENDERING
     * =========================================================================
     */
    function switchView(viewName) {
      document.querySelectorAll('.view-screen').forEach(el => el.classList.remove('active'));
      const targetView = document.getElementById(`view-${viewName}`);
      if (targetView) targetView.classList.add('active');

      // Update Nav active classes
      document.querySelectorAll('.nav-link, .mobile-nav-item').forEach(btn => {
        if (btn.dataset.view === viewName) {
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
        } else {
          btn.classList.remove('active');
          btn.setAttribute('aria-selected', 'false');
        }
      });

      // Render fresh data for view
      if (viewName === 'home') renderDashboard();
      if (viewName === 'library') renderLibrary();
      if (viewName === 'progress') renderProgressView();
      if (viewName === 'settings') renderSettingsView();

      window.scrollTo(0, 0);
    }

    /* Render Dashboard */
    function renderDashboard() {
      // Time-based greeting
      const hour = new Date().getHours();
      let greeting = 'Chào bạn! 👋';
      if (hour >= 5 && hour < 12) greeting = 'Chào buổi sáng! 🌅';
      else if (hour >= 12 && hour < 18) greeting = 'Chào buổi chiều! ☀️';
      else greeting = 'Chào buổi tối! 🌙';

      const greetingEl = document.getElementById('greeting-text');
      if (greetingEl) greetingEl.textContent = greeting;

      const dateEl = document.getElementById('current-date-text');
      if (dateEl) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateEl.textContent = new Date().toLocaleDateString('vi-VN', options);
      }

      // Stats
      const streak = AppState.user.streak || 0;
      const xp = AppState.user.xp || 0;
      const goal = AppState.user.dailyGoal || 10;
      const todayCount = AppState.user.todayLearnedCount || 0;

      document.getElementById('dash-streak-count').textContent = `${streak} ngày`;
      document.getElementById('dash-xp-count').textContent = `${xp} XP`;
      document.getElementById('dash-goal-text').textContent = `${todayCount} / ${goal} từ`;

      document.getElementById('mobile-streak-val').textContent = streak;
      document.getElementById('mobile-xp-val').textContent = xp;

      // Due words for SRS review
      const dueWords = SRSEngine.getDueWords();
      const dueDesc = document.getElementById('dash-due-count-desc');
      const dueBadge = document.getElementById('btn-due-counter-badge');

      if (dueWords.length > 0) {
        dueDesc.textContent = `Bạn có ${dueWords.length} từ đến hạn ôn tập hôm nay theo chu kỳ nhớ!`;
        dueBadge.textContent = `(${dueWords.length})`;
      } else {
        dueDesc.textContent = '🎉 Bạn đã hoàn thành hết từ đến hạn hôm nay! Có thể ôn tập tự do.';
        dueBadge.textContent = '(0)';
      }

      // Level progress quick pills
      ['B1', 'B2', 'C1'].forEach(level => {
        const total = AppState.vocabList.filter(w => w.level === level).length;
        const learned = AppState.vocabList.filter(w => w.level === level && (SRSEngine.getWordProgress(w.id).box > 0)).length;
        const percent = total > 0 ? Math.round((learned / total) * 100) : 0;

        const ratioEl = document.getElementById(`${level.toLowerCase()}-quick-ratio`);
        const barEl = document.getElementById(`${level.toLowerCase()}-quick-progress`);

        if (ratioEl) ratioEl.textContent = `${learned}/${total}`;
        if (barEl) barEl.style.width = `${percent}%`;
      });
    }

    /* Render Course Library */
    let currentCefrTab = 'B1';
    let searchQuery = '';

    function renderLibrary() {
      const grid = document.getElementById('library-topic-grid');
      if (!grid) return;

      // Filter words by level and search query
      const filteredWords = AppState.vocabList.filter(w => {
        const matchesLevel = searchQuery ? true : (w.level === currentCefrTab);
        if (!matchesLevel) return false;

        if (!searchQuery) return true;
        const q = searchQuery.toLowerCase();
        return (
          w.word.toLowerCase().includes(q) ||
          w.meaningVi.toLowerCase().includes(q) ||
          w.topic.toLowerCase().includes(q) ||
          w.definitionEn.toLowerCase().includes(q)
        );
      });

      // Group by topic
      const topicMap = {};
      filteredWords.forEach(w => {
        if (!topicMap[w.topic]) {
          topicMap[w.topic] = {
            name: w.topic,
            level: w.level,
            words: []
          };
        }
        topicMap[w.topic].words.push(w);
      });

      const topics = Object.values(topicMap);

      if (topics.length === 0) {
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px; background: var(--bg-card); border-radius: var(--radius-xl); border: 1px dashed var(--border-color);">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🔍</div>
            <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 4px;">Không tìm thấy từ nào</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted);">Hãy thử nhập từ khóa khác hoặc chuyển sang cấp độ khác.</p>
          </div>
        `;
        return;
      }

      // Topic icon helper
      const topicIcons = {
        'Du lịch & Đi lại': '✈️',
        'Đời sống & Cảm xúc': '😊',
        'Công việc & Nghề nghiệp': '💼',
        'Ẩm thực & Mua sắm': '🍜',
        'Môi trường & Bền vững': '🌿',
        'Công nghệ & Đổi mới': '💻',
        'Kinh tế & Kinh doanh': '📈',
        'Xã hội & Giáo dục': '🎓',
        'Học thuật & Tranh biện': '🏛️',
        'Chính sách & Thể chế': '⚖️',
        'Tâm lý & Nhận thức': '🧠',
        'Thành ngữ & Cụm nâng cao': '✨'
      };

      grid.innerHTML = topics.map(top => {
        const total = top.words.length;
        const learned = top.words.filter(w => SRSEngine.getWordProgress(w.id).box > 0).length;
        const percent = total > 0 ? Math.round((learned / total) * 100) : 0;
        const icon = topicIcons[top.name] || '📖';

        return `
          <div class="topic-card" data-topic-name="${top.name}">
            <div class="topic-header">
              <div class="topic-icon-wrap">${icon}</div>
              <div class="topic-meta">
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 2px;">
                  <span class="level-badge badge-${top.level.toLowerCase()}">${top.level}</span>
                  <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-sub);">${learned}/${total} từ</span>
                </div>
                <h3 class="topic-title">${top.name}</h3>
              </div>
            </div>

            <div class="progress-bar-bg">
              <div class="progress-bar-fill" style="width: ${percent}%;"></div>
            </div>

            <div class="topic-actions">
              <button class="btn-topic-learn" onclick="handleStartTopicLearn('${top.name}')">
                <span>▶ Học bộ này</span>
              </button>
              <button class="btn-topic-view" onclick="handleOpenTopicModal('${top.name}')">
                <span>👁 Xem từ</span>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    /* Topic Modal Preview */
    window.handleOpenTopicModal = function(topicName) {
      const topicWords = AppState.vocabList.filter(w => w.topic === topicName);
      if (!topicWords.length) return;

      const modal = document.getElementById('modal-topic-preview');
      const title = document.getElementById('topic-preview-title');
      const meta = document.getElementById('topic-preview-meta');
      const list = document.getElementById('topic-preview-words-list');
      const btnStart = document.getElementById('btn-modal-start-this-topic');

      title.textContent = topicName;
      meta.textContent = `${topicWords[0].level} • ${topicWords.length} từ vựng`;

      list.innerHTML = topicWords.map(w => {
        const prog = SRSEngine.getWordProgress(w.id);
        const status = SRSEngine.getStatus(w.id);
        return `
          <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 12px; display: flex; align-items: flex-start; justify-content: space-between; gap: 10px;">
            <div style="flex: 1; min-width: 0;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <strong style="font-size: 1.05rem; color: var(--text-main);">${w.word}</strong>
                <span style="font-size: 0.85rem; color: var(--primary); font-weight: 600;">${w.ipa}</span>
                <span style="font-size: 0.75rem; background: var(--bg-subtle); padding: 2px 6px; border-radius: 4px; color: var(--text-sub);">${w.pos}</span>
              </div>
              <div style="font-size: 0.88rem; font-weight: 700; color: var(--text-muted); margin-top: 3px;">${w.meaningVi}</div>
              <div style="font-size: 0.8rem; color: var(--text-sub); margin-top: 2px; font-style: italic;">"${w.example}"</div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 6px;">
              <span class="card-badge" style="background: var(--bg-subtle); color: var(--text-sub); font-size: 0.7rem;">${status}</span>
              <button class="flashcard-audio-btn" style="width: 34px; height: 34px; font-size: 14px; margin: 0;" onclick="AudioManager.speak('${w.word}')" aria-label="Phát âm ${w.word}">
                🔊
              </button>
            </div>
          </div>
        `;
      }).join('');

      btnStart.onclick = () => {
        modal.classList.remove('active');
        SessionEngine.startSession(topicWords, 'topic');
      };

      modal.classList.add('active');
    };

    window.handleStartTopicLearn = function(topicName) {
      const topicWords = AppState.vocabList.filter(w => w.topic === topicName);
      SessionEngine.startSession(topicWords, 'topic');
    };

    /* Render Progress View */
    function renderProgressView() {
      const totalLearned = AppState.vocabList.filter(w => SRSEngine.getWordProgress(w.id).box > 0).length;
      const totalMastered = AppState.vocabList.filter(w => SRSEngine.getWordProgress(w.id).box === 5).length;

      document.getElementById('prog-total-learned').textContent = totalLearned;
      document.getElementById('prog-total-mastered').textContent = totalMastered;
      document.getElementById('prog-streak-val').textContent = `${AppState.user.streak || 0} ngày`;
      document.getElementById('prog-xp-val').textContent = `${AppState.user.xp || 0} XP`;

      // Leitner box counts
      const boxCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
      Object.values(AppState.wordProgress).forEach(p => {
        if (p.box >= 1 && p.box <= 5) {
          boxCounts[p.box]++;
        }
      });

      for (let i = 1; i <= 5; i++) {
        const el = document.getElementById(`box-count-${i}`);
        if (el) el.textContent = boxCounts[i];
      }

      // Render 7-day barchart
      const chartContainer = document.getElementById('seven-days-barchart');
      if (!chartContainer) return;

      const days = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const iso = d.toISOString().slice(0, 10);
        const dayName = i === 0 ? 'Hôm nay' : ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'][d.getDay()];
        const entry = AppState.history.find(h => h.date === iso) || { xp: 0, wordsCount: 0 };
        days.push({ dayName, xp: entry.xp });
      }

      const maxXp = Math.max(50, ...days.map(d => d.xp));

      chartContainer.innerHTML = days.map(d => {
        const heightPercent = Math.min(100, Math.round((d.xp / maxXp) * 100));
        return `
          <div class="barchart-col">
            <span style="font-size: 0.72rem; font-weight: 700; color: var(--primary);">${d.xp > 0 ? d.xp : ''}</span>
            <div class="barchart-bar-bg" title="${d.dayName}: ${d.xp} XP">
              <div class="barchart-bar-inner" style="height: ${heightPercent}%;"></div>
            </div>
            <span class="barchart-label">${d.dayName}</span>
          </div>
        `;
      }).join('');
    }

    /* Render Settings View */
    function renderSettingsView() {
      // Toggle inputs
      document.getElementById('settings-dark-toggle').checked = AppState.user.theme === 'dark';
      document.getElementById('sidebar-dark-toggle').checked = AppState.user.theme === 'dark';
      document.getElementById('settings-speech-toggle').checked = AppState.user.speechEnabled;
      document.getElementById('settings-soundfx-toggle').checked = AppState.user.soundEffectsEnabled;

      // Font buttons
      document.querySelectorAll('[data-font-btn]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.fontBtn === AppState.user.fontSize);
      });

      // Goal buttons
      document.querySelectorAll('[data-goal-btn]').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.goalBtn) === AppState.user.dailyGoal);
      });

      // Vocab summary
      const total = AppState.vocabList.length;
      const b1 = AppState.vocabList.filter(w => w.level === 'B1').length;
      const b2 = AppState.vocabList.filter(w => w.level === 'B2').length;
      const c1 = AppState.vocabList.filter(w => w.level === 'C1').length;

      document.getElementById('settings-vocab-total-badge').textContent = `${total} từ`;
      document.getElementById('settings-vocab-summary').textContent = `B1: ${b1} từ • B2: ${b2} từ • C1: ${c1} từ`;
    }

    /* Theme & Font Apply Helpers */
    function applyTheme(theme) {
      AppState.user.theme = theme;
      document.documentElement.setAttribute('data-theme', theme);
      const darkToggle1 = document.getElementById('settings-dark-toggle');
      const darkToggle2 = document.getElementById('sidebar-dark-toggle');
      if (darkToggle1) darkToggle1.checked = theme === 'dark';
      if (darkToggle2) darkToggle2.checked = theme === 'dark';
      saveState();
    }

    function applyFontSize(size) {
      AppState.user.fontSize = size;
      document.documentElement.setAttribute('data-font', size);
      document.querySelectorAll('[data-font-btn]').forEach(b => {
        b.classList.toggle('active', b.dataset.fontBtn === size);
      });
      saveState();
    }

    /* Toast Helper */
    function showToast(msg) {
      const container = document.getElementById('toast-container');
      if (!container) return;
      const toast = document.createElement('div');
      toast.className = 'toast-pill';
      toast.innerHTML = `<span>✨</span><span>${msg}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 2600);
    }

    /**
     * =========================================================================
     * 8. EVENT LISTENERS & USER INTERACTIONS
     * =========================================================================
     */
    document.addEventListener('DOMContentLoaded', () => {
      initAppState();
      Confetti.init();
      renderDashboard();

      // Navigation clicks
      document.querySelectorAll('[data-view]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const view = btn.dataset.view;
          switchView(view);
        });
      });

      // Home CTA buttons
      document.getElementById('btn-start-continue-learn').addEventListener('click', () => {
        // Next 10 words (either unlearned or in progress)
        const newWords = SRSEngine.getNewWords(10);
        if (newWords.length > 0) {
          SessionEngine.startSession(newWords, 'learn');
        } else {
          // If all words started, review words that need work
          SessionEngine.startSession(AppState.vocabList.slice(0, 10), 'learn');
        }
      });

      document.getElementById('btn-start-due-review').addEventListener('click', () => {
        const dueWords = SRSEngine.getDueWords();
        if (dueWords.length > 0) {
          SessionEngine.startSession(dueWords, 'review');
        } else {
          showToast('🎉 Tuyệt vời! Bạn không có từ nào đến hạn. Đang mở phiên ôn tự do.');
          const anyWords = AppState.vocabList.slice(0, 10);
          SessionEngine.startSession(anyWords, 'review');
        }
      });

      document.getElementById('btn-go-library-all').addEventListener('click', () => {
        switchView('library');
      });

      document.querySelectorAll('[data-jump-level]').forEach(card => {
        card.addEventListener('click', () => {
          currentCefrTab = card.dataset.jumpLevel;
          document.querySelectorAll('.cefr-tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.cefrTab === currentCefrTab);
          });
          switchView('library');
        });
      });

      // Library search & tabs
      const searchInput = document.getElementById('library-search-input');
      const searchClear = document.getElementById('search-clear-btn');

      searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.trim();
        searchClear.style.display = searchQuery ? 'block' : 'none';
        renderLibrary();
      });

      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        searchClear.style.display = 'none';
        renderLibrary();
        searchInput.focus();
      });

      document.querySelectorAll('.cefr-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.cefr-tab-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentCefrTab = btn.dataset.cefrTab;
          renderLibrary();
        });
      });

      // Session Exit handling
      document.getElementById('btn-session-exit').addEventListener('click', () => {
        document.getElementById('modal-confirm-exit').classList.add('active');
      });

      document.getElementById('btn-cancel-exit-session').addEventListener('click', () => {
        document.getElementById('modal-confirm-exit').classList.remove('active');
      });

      document.getElementById('btn-confirm-exit-session').addEventListener('click', () => {
        document.getElementById('modal-confirm-exit').classList.remove('active');
        SessionState.active = false;
        switchView('home');
      });

      // Summary buttons
      document.getElementById('btn-summary-next-session').addEventListener('click', () => {
        const nextWords = SRSEngine.getNewWords(10);
        if (nextWords.length > 0) {
          SessionEngine.startSession(nextWords, 'learn');
        } else {
          SessionEngine.startSession(AppState.vocabList.slice(0, 10), 'learn');
        }
      });

      document.getElementById('btn-summary-home').addEventListener('click', () => {
        switchView('home');
      });

      // Settings Theme & Font
      document.getElementById('settings-dark-toggle').addEventListener('change', (e) => {
        applyTheme(e.target.checked ? 'dark' : 'light');
      });

      document.getElementById('sidebar-dark-toggle').addEventListener('change', (e) => {
        applyTheme(e.target.checked ? 'dark' : 'light');
      });

      document.querySelectorAll('[data-font-btn]').forEach(btn => {
        btn.addEventListener('click', () => {
          applyFontSize(btn.dataset.fontBtn);
        });
      });

      document.querySelectorAll('[data-goal-btn]').forEach(btn => {
        btn.addEventListener('click', () => {
          AppState.user.dailyGoal = parseInt(btn.dataset.goalBtn);
          saveState();
          renderSettingsView();
          renderDashboard();
          showToast(`Đã đổi mục tiêu: ${AppState.user.dailyGoal} từ/ngày`);
        });
      });

      document.getElementById('settings-speech-toggle').addEventListener('change', (e) => {
        AppState.user.speechEnabled = e.target.checked;
        saveState();
      });

      document.getElementById('settings-soundfx-toggle').addEventListener('change', (e) => {
        AppState.user.soundEffectsEnabled = e.target.checked;
        saveState();
      });

      // Vocabulary Management buttons
      document.getElementById('btn-open-import-modal').addEventListener('click', () => {
        document.getElementById('modal-import-vocab').classList.add('active');
      });

      document.getElementById('btn-close-import-modal').addEventListener('click', () => {
        document.getElementById('modal-import-vocab').classList.remove('active');
      });

      document.getElementById('btn-close-topic-modal').addEventListener('click', () => {
        document.getElementById('modal-topic-preview').classList.remove('active');
      });

      // 1-Click Load Extended Pack
      document.getElementById('btn-load-extended-pack').addEventListener('click', () => {
        let addedCount = 0;
        EXTENDED_PACK.forEach(item => {
          if (!AppState.vocabList.some(w => w.word.toLowerCase() === item.word.toLowerCase())) {
            AppState.vocabList.push(item);
            addedCount++;
          }
        });
        saveState();
        renderSettingsView();
        renderLibrary();
        showToast(`🚀 Đã nạp thành công ${addedCount} từ vựng mở rộng!`);
      });

      // JSON File import & Textarea import
      document.getElementById('import-file-input').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
          document.getElementById('import-json-textarea').value = event.target.result;
        };
        reader.readAsText(file);
      });

      document.getElementById('btn-submit-import-json').addEventListener('click', () => {
        const raw = document.getElementById('import-json-textarea').value.trim();
        if (!raw) {
          showToast('Vui lòng dán dữ liệu JSON hoặc chọn file!');
          return;
        }

        try {
          const parsed = JSON.parse(raw);
          if (!Array.isArray(parsed)) {
            showToast('Dữ liệu JSON phải là một mảng []!');
            return;
          }

          let added = 0;
          parsed.forEach((item, idx) => {
            if (item.word && item.meaningVi) {
              const cleanItem = {
                id: item.id || `custom-${Date.now()}-${idx}`,
                word: item.word.trim(),
                ipa: item.ipa || '',
                pos: item.pos || 'noun',
                meaningVi: item.meaningVi.trim(),
                definitionEn: item.definitionEn || '',
                example: item.example || '',
                exampleVi: item.exampleVi || '',
                level: (item.level || 'B1').toUpperCase(),
                topic: item.topic || 'Từ vựng bổ sung'
              };

              // Avoid exact duplicate
              if (!AppState.vocabList.some(w => w.word.toLowerCase() === cleanItem.word.toLowerCase())) {
                AppState.vocabList.push(cleanItem);
                added++;
              }
            }
          });

          saveState();
          document.getElementById('modal-import-vocab').classList.remove('active');
          document.getElementById('import-json-textarea').value = '';
          renderSettingsView();
          renderLibrary();
          showToast(`✅ Đã nạp thành công ${added} từ mới vào kho!`);
        } catch (err) {
          alert('Lỗi phân tích cú pháp JSON! Vui lòng kiểm tra lại định dạng:\\n' + err.message);
        }
      });

      // Export Vocab JSON
      document.getElementById('btn-export-vocab-json').addEventListener('click', () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(AppState.vocabList, null, 2));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", "lexiup-vocab.json");
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
        showToast('📥 Đã tải xuống file lexiup-vocab.json');
      });

      // Reset Progress Modal
      let resetMode = 'progress';
      document.getElementById('btn-reset-progress-modal').addEventListener('click', () => {
        resetMode = 'progress';
        document.getElementById('reset-confirm-title').textContent = 'Đặt lại tiến độ học?';
        document.getElementById('reset-confirm-desc').textContent = 'Tất cả trạng thái từ vựng sẽ trở về "Mới" và chuỗi học tập sẽ đặt lại về 0. Kho từ vựng vẫn được giữ nguyên.';
        document.getElementById('modal-confirm-reset').classList.add('active');
      });

      document.getElementById('btn-factory-reset').addEventListener('click', () => {
        resetMode = 'factory';
        document.getElementById('reset-confirm-title').textContent = '⚠️ Khôi phục cài đặt gốc?';
        document.getElementById('reset-confirm-desc').textContent = 'Toàn bộ tiến độ, lịch sử và từ vựng tùy chỉnh sẽ bị xóa sạch, đưa ứng dụng về 90 từ mặc định ban đầu.';
        document.getElementById('modal-confirm-reset').classList.add('active');
      });

      document.getElementById('btn-cancel-reset').addEventListener('click', () => {
        document.getElementById('modal-confirm-reset').classList.remove('active');
      });

      document.getElementById('btn-execute-reset').addEventListener('click', () => {
        document.getElementById('modal-confirm-reset').classList.remove('active');
        if (resetMode === 'progress') {
          AppState.wordProgress = {};
          AppState.user.streak = 0;
          AppState.user.todayLearnedCount = 0;
          saveState();
          renderDashboard();
          renderProgressView();
          showToast('🔄 Đã đặt lại toàn bộ tiến độ học!');
        } else {
          StorageManager.clear();
          location.reload();
        }
      });

      // Keyboard Accessibility: Shortcuts (1, 2, 3, 4, Space, Enter, Escape)
      document.addEventListener('keydown', (e) => {
        // Esc: close modals
        if (e.key === 'Escape') {
          document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
          return;
        }

        // Quiz shortcuts
        if (SessionState.active && !SessionState.isAnswered) {
          if (['1', '2', '3', '4'].includes(e.key)) {
            const index = parseInt(e.key) - 1;
            const buttons = document.querySelectorAll('.quiz-option-btn');
            if (buttons[index]) {
              buttons[index].click();
            }
          }

          // Space: Flip flashcard if intro
          if (e.key === ' ' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            const card = document.getElementById('session-flip-card');
            if (card) {
              e.preventDefault();
              card.classList.toggle('is-flipped');
            }
          }
        }
      });
    });
  </script>
</body>
</html>
"""

HTML_CONTENT = HTML_CONTENT.replace('__VOCAB_JSON__', vocab_json).replace('__EXTENDED_JSON__', extended_json)

# Write index.html
output_html_path = r"C:\Users\vanh\.gemini\antigravity\scratch\lexiup\index.html"
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated index.html at {output_html_path} ({len(HTML_CONTENT)} bytes)")
