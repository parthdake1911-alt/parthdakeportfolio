"""Slides and Upwork text for each project pack (used by make_upwork.py)."""

B, P, X = 'browser', 'phone', 'plain'

PROJECTS = [
  {
    'slug': 'Tata-Power-Customer-Smile', 'folder': 'tatapower', 'bg': '#EAF1FB', 'logo': 'logos/tata.png', 'lh': 64,
    'kicker': 'Client project · Mobile app', 'title_short': 'Customer Smile',
    'subtitle': 'An internal employee app for Tata Power · end-to-end UX/UI',
    'slides': [
      {'cover': True, 'kind': P, 'img': ['tata/out/t_explore.webp', 'tata/out/t_home.webp', 'tata/out/t_champions.webp']},
      {'file': 'four-roles', 'title': 'One app, four roles: every review step visible to the employee',
       'items': [('tata/out/t_status.webp', P), ('tata/out/t_bin.webp', P), ('tata/out/t_dates.webp', P)]},
      {'file': 'share-in-three-steps', 'title': 'Sharing a customer story in three quick steps',
       'items': [('tata/out/t_chooser.webp', P), ('tata/out/t_quick_filled.webp', P), ('tata/out/t_success.webp', P)]},
      {'file': 'guided-writing', 'title': 'Guided prompts, AI drafting and voice input for the full story',
       'items': [('tata/out/t_share_mid.webp', P), ('tata/out/t_share_listen.webp', P)]},
      {'file': 'gamification', 'title': 'Gamification tied to the real task: points, a daily spin, recognition',
       'items': [('tata/out/t_spin.webp', P), ('tata/out/t_home_prog.webp', P), ('tata/out/t_champions_pc.webp', P)]},
      {'file': 'recognition', 'title': 'Peer recognition built into every story',
       'items': [('tata/out/t_story.webp', P), ('tata/out/t_react.webp', P), ('tata/out/t_notif.webp', P)]},
    ],
    'text': """
PROJECT TITLE
Tata Power Customer Smile – Employee Mobile App (UX/UI)

YOUR ROLE
UX/UI Designer (end-to-end)

PROJECT DESCRIPTION
Customer Smile is an internal Tata Power platform where employees share stories of customers they helped. The client wanted the existing website turned into an intuitive mobile app for four roles (employees, managers, administrators and jury members) and to explore gamification. I mapped the role workflows, wireframed and designed the UI in Figma, and built a working prototype with Claude, iterating with the client throughout.

SKILLS (pick up to 5)
Mobile App Design · UX & UI · User Flow · Figma · Prototyping
""",
  },
  {
    'slug': 'ICA-Premium-Website-Redesign', 'folder': 'ica', 'bg': '#F2EFEA', 'logo': 'logos/ica.png', 'lh': 84,
    'kicker': 'Client project · Website redesign', 'title_short': 'ICA Italian Wood Finishes',
    'subtitle': 'A more premium homepage, informed by luxury-brand references',
    'slides': [
      {'cover': True, 'kind': B, 'img': 'ica/out/i_hero3.webp'},
      {'file': 'first-impression', 'title': 'A stronger first impression: full-screen hero, one clear message',
       'items': [('ica/out/i_hero1.webp', B), ('ica/out/i_loader.webp', B)]},
      {'file': 'visual-storytelling', 'title': 'Materials and craft tell the story',
       'items': [('ica/out/i_trend.webp', B), ('ica/out/i_mosaic.webp', B)]},
      {'file': 'typography', 'title': 'Restrained typography: light weights, one headline pattern',
       'items': [('ica/out/c_type_sand.webp', X), ('ica/out/c_type_fin.webp', X)]},
      {'file': 'layout', 'title': 'Full-height sections paced like a presentation',
       'items': [('ica/out/i_exp1.webp', B), ('ica/out/i_hl.webp', B)]},
      {'file': 'navigation', 'title': 'Clarity within a premium aesthetic: menu and search',
       'items': [('ica/out/i_menu.webp', B), ('ica/out/i_search.webp', B)]},
      {'file': 'mobile', 'title': 'The direction holds up on a phone',
       'items': [('ica/out/m_hero.webp', P), ('ica/out/m_mosaic.webp', P), ('ica/out/m_exppin.webp', P)]},
    ],
    'text': """
PROJECT TITLE
ICA Italian Wood Finishes – Premium Website Redesign

YOUR ROLE
UX/UI Designer

PROJECT DESCRIPTION
ICA wanted a website that felt more luxurious and premium. I studied luxury-brand websites (including Jaguar and Balenciaga) for their approach to imagery, typography, whitespace and storytelling, then translated those principles into a new homepage direction for ICA: a full-screen hero, material-led visual storytelling, restrained typography and a calm, section-by-section layout, delivered as an interactive prototype.

SKILLS (pick up to 5)
Web Design · UX & UI · Landing Page Design · Competitive Analysis · Prototyping
""",
  },
  {
    'slug': 'AMIN-Worldwide-Member-Portal', 'folder': 'amin', 'bg': '#F1EEFB', 'logo': 'logos/amin.png', 'lh': 46,
    'kicker': 'Pitch project · Portal redesign', 'title_short': 'AMIN Worldwide',
    'subtitle': 'Member portal: UX audit, redesign and a clickable prototype',
    'slides': [
      {'cover': True, 'kind': B, 'img': 'amin/out/a_globe.webp'},
      {'file': 'dashboard', 'title': 'A home page that shows what matters to each member',
       'items': [('amin/out/a_dash.webp', B)]},
      {'file': 'directory-before-after', 'title': '1,912 members, and the old directory showed none of them',
       'labels': ['Before · current portal', 'After · my redesign'],
       'items': [('amin/out/before_05.webp', X), ('amin/out/a_mgrid.webp', B)]},
      {'file': 'events-before-after', 'title': 'Finding the relevant event, without manual searching',
       'labels': ['Before · current portal', 'After · my redesign'],
       'items': [('amin/out/before_06.webp', X), ('amin/out/a_events.webp', B)]},
      {'file': 'library-before-after', 'title': 'Valuable content no longer hidden behind the word “HERE”',
       'labels': ['Before · current portal', 'After · my redesign'],
       'items': [('amin/out/before_07.webp', X), ('amin/out/a_library.webp', B)]},
      {'file': 'search-and-posting', 'title': 'One search across the whole network, posting in one click',
       'items': [('amin/out/a_search.webp', B), ('amin/out/a_create.webp', X)]},
    ],
    'text': """
PROJECT TITLE
AMIN Worldwide – Member Portal UX Audit & Redesign

YOUR ROLE
UX Auditor, UX/UI Designer & Prototyper (pitch project)

PROJECT DESCRIPTION
AMIN Worldwide is a global network of independent agencies. I audited its member portal, found seven issues that made everyday tasks hard (a buried directory, manual event hunting, hidden content, confusing profiles) and redesigned the experience around the members who use it. I designed wireframes in Figma and used Claude to build a working prototype, plus a short walkthrough video. This was a pitch, not a launched product.

SKILLS (pick up to 5)
UX Audit · UX & UI · Web App Design · Figma · Prototyping
""",
  },
  {
    'slug': 'Anchor-Trading-Journal-App', 'folder': 'anchor', 'bg': '#EEF2F9', 'logo': 'logos/anchor.svg', 'lh': 58,
    'kicker': 'Graduation project · Desktop app', 'title_short': 'Anchor',
    'subtitle': 'A trading journal that brings trading data into focus',
    'slides': [
      {'cover': True, 'kind': B, 'img': 'anchor/out/a_dash.webp'},
      {'file': 'dashboard', 'title': 'The dashboard starts with what needs doing, then what happened',
       'col': True, 'items': [('anchor/out/c_queue.webp', X), ('anchor/out/c_kpis.webp', X), ('anchor/out/a_rep_overview.webp', B)]},
      {'file': 'trade-table', 'title': 'A trade table built to be scanned row by row',
       'items': [('anchor/out/a_trades.webp', B)]},
      {'file': 'charts', 'title': 'Charts that explain themselves, and one score with its working shown',
       'items': [('anchor/out/c_daily.webp', X), ('anchor/out/c_score.webp', X)]},
      {'file': 'rules', 'title': 'Every trade checked against the rules the trader set',
       'items': [('anchor/out/a_wizard2.webp', B), ('anchor/out/a_strategy_detail.webp', B)]},
      {'file': 'review', 'title': 'One page to review a trade, a journal to review the day',
       'items': [('anchor/out/c_tradeside.webp', X), ('anchor/out/a_journal.webp', B)]},
      {'file': 'dark-mode', 'title': 'A focused workspace, in light and dark',
       'items': [('anchor/out/a_dark.webp', B)]},
    ],
    'text': """
PROJECT TITLE
Anchor – Trading Journal Desktop App (UX/UI)

YOUR ROLE
UX/UI Designer (graduation project)

PROJECT DESCRIPTION
Anchor is a desktop trading-data management system that helps traders organise their trades, track performance and understand their activity. I structured the information around the trader's daily workflow: a task-first dashboard, scannable trade tables, self-explaining charts, rule checks against the trader's own strategy, and a daily journal. Designed in Figma and built into a working prototype with Claude.

SKILLS (pick up to 5)
Dashboard Design · UX & UI · Data Visualization · Figma · Prototyping
""",
  },
  {
    'slug': 'Ellenbarrie-Homepage-Redesign', 'folder': 'ellenbarrie', 'bg': '#F8EEEE', 'logo': 'logos/ellenbarrie.png', 'lh': 64,
    'kicker': 'Pitch project · UX audit', 'title_short': 'Ellenbarrie',
    'subtitle': 'A clearer homepage for an industrial gas company',
    'slides': [
      {'cover': True, 'kind': B, 'img': 'ellen/out/r_hero.webp'},
      {'file': 'hero-before-after', 'title': 'Say who Ellenbarrie is before anything else',
       'labels': ['Before · current homepage', 'After · my redesign'],
       'items': [('ellen/out/o_hero.webp', B), ('ellen/out/r_hero.webp', B)]},
      {'file': 'services-before-after', 'title': 'From six scattered cards to one story about what they do',
       'labels': ['Before · current homepage', 'After · my redesign'],
       'items': [('ellen/out/o_services.webp', X), ('ellen/out/r_services.webp', B)]},
      {'file': 'key-figures', 'title': 'Turning a paragraph into four figures you can’t miss',
       'items': [('ellen/out/r_why.webp', B)]},
      {'file': 'visual-system', 'title': 'Bolder type, more contrast, and red only where it matters',
       'items': [('ellen/out/r_intro.webp', B), ('ellen/out/r_services2.webp', B)]},
    ],
    'text': """
PROJECT TITLE
Ellenbarrie Industrial Gases – Homepage UX Audit & Redesign

YOUR ROLE
UX/UI Designer (pitch project)

PROJECT DESCRIPTION
I audited the homepage of Ellenbarrie, an industrial gases company, and redesigned it as a pitch. The audit found a crowded top bar, ten competing calls to action and key facts buried in paragraphs. The redesign says who Ellenbarrie is up front, turns scattered service cards into one clear story, surfaces four key figures and gives visitors one clear next step. Delivered as an interactive HTML prototype.

SKILLS (pick up to 5)
UX Audit · Web Design · Landing Page Design · UX & UI · Prototyping
""",
  },
  {
    'slug': 'UltraTech-Home-Building-Journey', 'folder': 'ultratech', 'bg': '#FAF6E4', 'logo': 'logos/ultratech.png', 'lh': 64,
    'kicker': 'Mobile UX design', 'title_short': 'UltraTech Cement',
    'subtitle': 'Guiding people through the journey of building a home',
    'slides': [
      {'cover': True, 'kind': P, 'img': ['ultra/out/u_hero.webp']},
      {'file': 'seven-stages', 'title': 'Seven clear stages instead of one long block of content',
       'items': [('ultra/out/u_stages.webp', X)]},
      {'file': 'audio-guidance', 'title': 'Construction explained with pictures and a voice, in Hindi or English',
       'items': [('ultra/out/u_audio.webp', X)]},
    ],
    'text': """
PROJECT TITLE
UltraTech Cement – Home-Building Journey (Mobile UX)

YOUR ROLE
UX/UI Designer

PROJECT DESCRIPTION
Building a home comes with many questions. I designed a mobile-first experience that guides people through the home-building journey in seven clear stages, combining visual storytelling with spoken explanations in Hindi and English, so the process is easier to follow. Only selected screens are shown for confidentiality.

SKILLS (pick up to 5)
Mobile UX Design · UX & UI · Information Architecture · User Flow · Figma
""",
  },
  {
    'slug': 'Casagrand-Homepage-Redesign', 'folder': 'casagrand', 'bg': '#FBF3E3', 'logo': 'logos/casagrand.png', 'lh': 58,
    'kicker': 'Pitch project · Real-estate website', 'title_short': 'Casagrand',
    'subtitle': 'A homepage that helps families choose a home',
    'slides': [
      {'cover': True, 'kind': 'browser', 'img': 'casa/out/c_hero.webp'},
      {'file': 'homes-by-city', 'title': 'Start with a city: five cities, one simple index',
       'items': [('casa/out/c_cities.webp', 'browser')]},
      {'file': 'project-cards', 'title': 'Price, BHK and possession date on every project card',
       'items': [('casa/out/c_homes.webp', 'browser')]},
      {'file': 'promised-vs-delivered', 'title': 'Trust from a record buyers can check: promised vs delivered',
       'items': [('casa/out/c_proof.webp', 'browser')]},
      {'file': 'emi-planner', 'title': 'Help deciding: an EMI planner that reads like a sentence',
       'items': [('casa/out/c_help.webp', 'browser')]},
      {'file': 'book-a-visit', 'title': 'Booking a site visit takes under a minute',
       'items': [('casa/out/c_visit.webp', 'browser')]},
      {'file': 'mobile', 'title': 'Designed for the phone, with Call, WhatsApp and Book visit always at hand',
       'items': [('casa/out/m_hero.webp', 'phone'), ('casa/out/m_homes.webp', 'phone'), ('casa/out/m_help.webp', 'phone')]},
    ],
    'text': """
PROJECT TITLE
Casagrand – Real-Estate Homepage Redesign (UX/UI)

YOUR ROLE
UX/UI Designer (pitch project)

PROJECT DESCRIPTION
A homepage redesign pitch for Casagrand, a real-estate developer. I built the page around a homebuyer's questions: search by city, budget and possession; project cards with price and possession up front; a promised-vs-delivered handover record; an EMI planner; and a quick site-visit booking. Designed in Figma for desktop and mobile; I built the interactive prototype with Claude. Figures shown are placeholders.

SKILLS (pick up to 5)
Web Design · UX & UI · Landing Page Design · Figma · Prototyping
""",
  },
]
