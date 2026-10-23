/* ══════════════════════════════════════════
   THE NINE: player data. Edit numbers here; cards, pop-ups and the stats table all update.
   comps: one row per competition in 2026. Use null when a number isn't published.
   ══════════════════════════════════════════ */
var STATS_ASOF = '23 Oct 2026';
var ninePlayers = [
  {
    name:'Marsel Bibishkov', first:'Marsel', last:'Bibishkov', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1417560/marsel-bibishkov'},{t:'Wikipedia (Langley United loan)',u:'https://en.wikipedia.org/wiki/Marsel_Bibishkov'}], pos:'Striker / Left Wing', short:'ST', jersey:'19',
    club:'Vancouver FC', clubCode:'VFC', league:'CPL',
    ig:'https://www.instagram.com/marsel.bibishkov/', igHandle:'@marsel.bibishkov',
    photo:IMG.bibishkov, alt:'Marsel Bibishkov in a green club kit',
    comps:[
      {c:'CPL', apps:1, starts:0, mins:1, g:0, a:0},
      {c:'Canada U-20 · CONCACAF U-20 Championship', apps:4, starts:null, mins:174, g:0, a:1},
      {c:'Langley United (loan) · League1 BC', apps:1, starts:null, mins:null, g:1, a:0}
    ],
    stats:[{l:'Finishing',v:86},{l:'Strength',v:84},{l:'Aerial',v:85},{l:'Dribbling',v:79},{l:'Pace',v:78}],
    highlights:[
      '🇨🇦 Canada U-20 at the 2026 CONCACAF U-20 Championship (assist vs Mexico)',
      '⭐ Signed by Vancouver FC, March 2026',
      '🌍 Juventus U17: 17 apps, 6 goals (Italy)',
      '🇧🇬 Bulgarian top-flight debut with Septemvri Sofia',
      '🍁 TFC Academy graduate'
    ]
  },
  {
    name:'Tavio Ciccarelli', first:'Tavio', last:'Ciccarelli', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1780322/tavio-ciccarelli'}], pos:'Centre Forward', short:'ST', jersey:'20',
    club:'HFX Wanderers FC', clubCode:'HFX', league:'CPL', agency:'Rabonasports', from:'Winnipeg, MB',
    ig:'https://www.instagram.com/taviociccarelli/', igHandle:'@taviociccarelli',
    photo:IMG.ciccarelli, alt:'Tavio Ciccarelli in an HFX Wanderers kit',
    comps:[{c:'CPL', apps:22, starts:5, mins:480, g:6, a:0}],
    stats:[{l:'Finishing',v:87},{l:'Pace',v:84},{l:'Strength',v:80},{l:'Dribbling',v:82},{l:'Stamina',v:81}],
    highlights:[
      '🔥 6 CPL goals in 2026: one every 80 minutes',
      '🏆 CPL Team of the Week, Week 11',
      '⚽ Scored off the bench at Forge (3 Oct)',
      '🇨🇦 Canada U-20, 2024 CONCACAF U-20 Championship',
      '🌍 Former Sheffield United U18'
    ]
  },
  {
    name:'Kevaughn Tavernier', first:'Kevaughn', last:'Tavernier', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1609746/kevaughn-tavernier'}], pos:'Right Wing', short:'RW', jersey:'20',
    club:'Forge FC', clubCode:'FOR', league:'CPL',
    ig:'https://www.instagram.com/kj_tav/', igHandle:'@kj_tav',
    photo:IMG.tavernier, alt:'Kevaughn Tavernier in a red Canada national team kit',
    news:'Forge FC are 2026 Canadian Champions (21 Oct)',
    comps:[
      {c:'CPL', apps:3, starts:2, mins:127, g:0, a:0},
      {c:'CONCACAF Champions Cup', apps:2, starts:0, mins:5, g:0, a:0}
    ],
    stats:[{l:'Pace',v:90},{l:'Dribbling',v:86},{l:'Crossing',v:82},{l:'Finishing',v:77},{l:'Stamina',v:80}],
    highlights:[
      '🏆 2026 Canadian Champions with Forge FC: the first CPL club ever to win it',
      '🌍 CONCACAF Champions Cup minutes vs Tigres UANL',
      '⭐ Rejoined Forge FC on a multi-year pro deal (Jan 2026)',
      '🏆 League1 Ontario Young Player of the Season',
      '🇨🇦 Canada U-17 FIFA World Cup 2023',
      '🌍 Trialled at AS Monaco'
    ]
  },
  {
    name:'Zayne Bruno', first:'Zayne', last:'Bruno', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1610143/zayne-bruno'}], pos:'Central Midfield', short:'CM', jersey:'32',
    club:'Forge FC', clubCode:'FOR', league:'CPL',
    ig:'https://www.instagram.com/zaynebruno10/', igHandle:'@zaynebruno10',
    photo:IMG.bruno, alt:'Zayne Bruno in an orange Forge FC kit',
    news:'Forge FC are 2026 Canadian Champions (21 Oct)',
    comps:[
      {c:'CPL', apps:3, starts:0, mins:3, g:0, a:0},
      {c:'Canada U-20 (incl. CONCACAF U-20 Championship)', apps:8, starts:null, mins:null, g:1, a:1}
    ],
    stats:[{l:'Stamina',v:84},{l:'Passing',v:81},{l:'Tackling',v:78},{l:'Vision',v:79},{l:'Shooting',v:72}],
    highlights:[
      '🏆 2026 Canadian Champions with Forge FC: the first CPL club ever to win it',
      '🇨🇦 Canada U-20: 8 caps and a goal in 2026',
      '⭐ Forge FC Exceptional Young Player contract',
      '🔥 Youngest player on Forge FC first team (2025)',
      '🏆 League2 Ontario All-Star with Sigma FC B'
    ]
  },
  {
    name:'Lucas Olguin', first:'Lucas', last:'Olguin', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1780465/lucas-olguin'}], pos:'Central Midfield', short:'CM', jersey:'5',
    club:'HFX Wanderers FC', clubCode:'HFX', league:'CPL', from:'Toronto, ON',
    ig:'https://www.instagram.com/lucasolguinn8/', igHandle:'@lucasolguinn8',
    photo:IMG.olguin, alt:'Lucas Olguin in an HFX Wanderers kit',
    news:'First professional goal: 44′ at Vancouver FC, 17 Oct 2026',
    comps:[{c:'CPL', apps:22, starts:20, mins:1705, g:1, a:0}],
    stats:[{l:'Stamina',v:88},{l:'Passing',v:83},{l:'Vision',v:81},{l:'Tackling',v:82},{l:'Dribbling',v:80}],
    highlights:[
      '⚽ First professional goal: 44′ equaliser at Vancouver FC (17 Oct)',
      '⭐ 20 CPL starts in his first HFX season',
      '🔥 74 appearances for Toronto FC II',
      '🍁 TFC Academy graduate'
    ]
  },
  {
    name:'Sami Keshavarz', first:'Sami', last:'Keshavarz', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1780377/sami-keshavarz'}], pos:'Central Midfield', short:'CM', jersey:'34',
    club:'Pacific FC', clubCode:'PFC', league:'CPL',
    ig:'https://www.instagram.com/keshavarz___sam', igHandle:'@keshavarz___sam',
    photo:IMG.keshavarz, alt:'Sami Keshavarz in a purple Pacific FC kit',
    comps:[{c:'CPL', apps:11, starts:6, mins:554, g:0, a:0}],
    stats:[{l:'Stamina',v:85},{l:'Passing',v:82},{l:'Dribbling',v:79},{l:'Vision',v:80},{l:'Tackling',v:77}],
    highlights:[
      '🔥 Full 90s in Pacific’s 4–3 and 5–0 wins (Sep–Oct)',
      '⭐ Pacific FC professional contract',
      '🌍 Trained with VfL Bochum U-21 (Germany)'
    ]
  },
  {
    name:'Christian Greco-Taylor', first:'Christian', last:'Greco-Taylor', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1500408/christian-greco-taylor'}], pos:'Left Back', short:'LB', jersey:'15',
    club:'Pacific FC', clubCode:'PFC', league:'CPL', from:'Calgary, AB',
    ig:'https://www.instagram.com/cgrecotaylorr/', igHandle:'@cgrecotaylorr',
    photo:IMG.greco, alt:'Christian Greco-Taylor in a purple Pacific FC kit',
    comps:[{c:'CPL', apps:24, starts:18, mins:1733, g:0, a:2}],
    stats:[{l:'Defending',v:83},{l:'Pace',v:81},{l:'Stamina',v:85},{l:'Passing',v:76},{l:'Tackling',v:82}],
    highlights:[
      '⭐ 24 CPL appearances, 18 starts and 2 assists in 2026',
      '🇨🇦 Canada U-20 international',
      '📺 Featured in the CPL Next Gen series'
    ]
  },
  {
    name:'Ivan Pavela', first:'Ivan', last:'Pavela', src:[{t:'FotMob',u:'https://www.fotmob.com/players/1780385/ivan-pavela'}], pos:'Goalkeeper', short:'GK', jersey:'12',
    club:'Inter Toronto FC', clubCode:'ITO', league:'CPL', agency:'Rabonasports',
    ig:'https://www.instagram.com/ivanpavela/', igHandle:'@ivanpavela',
    photo:IMG.pavela, alt:'Ivan Pavela in a yellow Inter Toronto FC goalkeeper kit',
    gk:{saves:30, ga:18, cs:0},
    comps:[{c:'CPL', apps:7, starts:7, mins:630, g:0, a:0}],
    stats:[{l:'Reflexes',v:84},{l:'Positioning',v:82},{l:'Aerial',v:85},{l:'Distribution',v:78},{l:'Command',v:80}],
    highlights:[
      '🧤 30 CPL saves in 2026',
      '🏆 CPL Team of the Week, Week 18',
      '⭐ CPL Next Gen Class of 2025',
      '🇨🇦 Canada U-20 international',
      '🌍 Hajduk Split U19 and Puskás Akadémia U19'
    ]
  }
];
window.ninePlayers = ninePlayers;
