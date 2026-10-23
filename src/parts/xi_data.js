  /* ── PLAYER DATA ── edit numbers here to refresh the pitch cards and the Players & Stats table */
  var xiPlayers = [
    // 0 LW - CONFIRMED: Marsel Bibishkov
    {
      name:'Marsel Bibishkov',pos:'Left Wing (Natural CF)',short:'LW',jersey:'19',confirmed:true,
      club:'Vancouver FC - CPL',
      ig:'https://www.instagram.com/marsel.bibishkov/',igHandle:'@marsel.bibishkov',initials:'MB',
      photo:IMG.bibishkov, alt:'Marsel Bibishkov headshot in a green club kit',
      season:{comp:'CPL 2026',apps:1,starts:0,mins:1,g:0,a:0},
      extra:'Canada U-20 at the 2026 CONCACAF U-20 Championship: 4 apps, 1 assist.',
      stats:[{l:'Finishing',v:86},{l:'Strength',v:84},{l:'Aerial',v:85},{l:'Dribbling',v:79},{l:'Pace',v:78}],
      accolades:[
        '🇨🇦 Canada U-20 - 2026 CONCACAF U-20 Championship',
        '⚽ Natural position: Centre Forward',
        '🌍 Juventus U17 - 17 apps, 6 goals (Italy)',
        '🇧🇬 Septemvri Sofia - Bulgarian top flight debut',
        '⭐ Vancouver FC - signed March 2026',
        '🍁 TFC Academy graduate - chose to represent Canada'
      ]
    },
    // 1 CF - CONFIRMED: Tavio Ciccarelli
    {
      name:'Tavio Ciccarelli',pos:'Centre Forward',short:'CF',jersey:'20',confirmed:true,agency:'Rabonasports',
      club:'HFX Wanderers FC - CPL',
      ig:'https://www.instagram.com/taviociccarelli/',igHandle:'@taviociccarelli',initials:'TC',
      photo:IMG.ciccarelli, alt:'Tavio Ciccarelli headshot in an HFX Wanderers kit',
      season:{comp:'CPL 2026',apps:21,starts:5,mins:471,g:6,a:0},
      stats:[{l:'Finishing',v:87},{l:'Pace',v:84},{l:'Strength',v:80},{l:'Dribbling',v:82},{l:'Stamina',v:81}],
      accolades:[
        '🔥 6 CPL goals in 2026 - one every 79 minutes',
        '🏆 CPL Team of the Week - Week 11 (2026)',
        '⚽ Hat-trick vs. St. Vincent (Canada U-20 qualifiers)',
        '🇨🇦 Canada U-20 - 2024 CONCACAF U-20 Championship',
        '🌍 Former Sheffield United U18',
        '🍁 From Winnipeg, Manitoba'
      ]
    },
    // 2 RW - CONFIRMED: Tavernier
    {
      name:'Kevaughn Tavernier',pos:'Right Wing',short:'RW',jersey:'20',confirmed:true,
      club:'Forge FC - CPL',
      ig:'https://www.instagram.com/kj_tav/',igHandle:'@kj_tav',initials:'KT',
      photo:IMG.tavernier, alt:'Kevaughn Tavernier headshot in a red Canada national team kit',
      season:{comp:'CPL 2026',apps:3,starts:2,mins:127,g:0,a:0},
      extra:'CONCACAF Champions Cup 2026: 2 apps vs. Tigres UANL.',
      stats:[{l:'Pace',v:90},{l:'Dribbling',v:86},{l:'Crossing',v:82},{l:'Finishing',v:77},{l:'Stamina',v:80}],
      accolades:[
        '⭐ Rejoined Forge FC on a multi-year pro deal (Jan 2026)',
        '🏆 League1 Ontario Young Player of the Season',
        '🔥 15G in 15 matches - L1O Second Team All-Star',
        '🌍 3rd youngest Canadian to score in CONCACAF Champions Cup',
        '🇨🇦 Canada U-17 FIFA World Cup 2023 (Indonesia)',
        '🌍 Trialed at AS Monaco (Ligue 1)'
      ]
    },
    // 3 CM - CONFIRMED: Bruno
    {
      name:'Zayne Bruno',pos:'Central Midfielder',short:'CM',jersey:'32',confirmed:true,
      club:'Forge FC - CPL',
      ig:'https://www.instagram.com/zaynebruno10/',igHandle:'@zaynebruno10',initials:'ZB',
      photo:IMG.bruno, alt:'Zayne Bruno headshot in an orange Forge FC kit',
      season:{comp:'CPL 2026',apps:3,starts:0,mins:3,g:0,a:0},
      extra:'Canada U-20 at the 2026 CONCACAF U-20 Championship: 5 apps, 1 assist.',
      stats:[{l:'Stamina',v:84},{l:'Passing',v:81},{l:'Tackling',v:78},{l:'Vision',v:79},{l:'Shooting',v:72}],
      accolades:[
        '🇨🇦 Canada U-20 - 2026 CONCACAF U-20 Championship',
        '🇨🇦 Canada U-18 National Team call-up (Aug 2025)',
        '⭐ Forge FC Exceptional Young Player Contract',
        '🔥 Youngest player on Forge FC first team (2025)',
        '🏆 League2 Ontario All-Star - Sigma FC B'
      ]
    },
    // 4 RCM - CONFIRMED: Lucas Olguin
    {
      name:'Lucas Olguin',pos:'Right Centre Mid',short:'RCM',jersey:'5',confirmed:true,
      club:'HFX Wanderers FC - CPL',
      ig:'https://www.instagram.com/lucasolguinn8/',igHandle:'@lucasolguinn8',initials:'LO',
      photo:IMG.olguin, alt:'Lucas Olguin headshot in an HFX Wanderers kit',
      season:{comp:'CPL 2026',apps:21,starts:19,mins:1617,g:0,a:0},
      stats:[{l:'Stamina',v:88},{l:'Passing',v:83},{l:'Vision',v:81},{l:'Tackling',v:82},{l:'Dribbling',v:80}],
      accolades:[
        '⭐ 19 CPL starts and 1,617 minutes in his first HFX season',
        '🔥 74 appearances for Toronto FC II (MLS Next Pro)',
        '🍁 From Toronto, Ontario - TFC Academy graduate'
      ]
    },
    // 5 LCM - CONFIRMED: Keshavarz
    {
      name:'Sami Keshavarz',pos:'Left Centre Mid',short:'LCM',jersey:'34',confirmed:true,
      club:'Pacific FC - CPL',
      ig:'https://www.instagram.com/keshavarz___sam',igHandle:'@keshavarz___sam',initials:'SK',
      photo:IMG.keshavarz, alt:'Sami Keshavarz headshot in a purple and black Pacific FC kit',
      season:{comp:'CPL 2026',apps:10,starts:5,mins:464,g:0,a:0},
      stats:[{l:'Stamina',v:85},{l:'Passing',v:82},{l:'Dribbling',v:79},{l:'Vision',v:80},{l:'Tackling',v:77}],
      accolades:[
        '⭐ Pacific FC professional contract',
        '🌍 VfL Bochum U-21 training (Germany)',
        '🔥 10 CPL appearances, 5 starts in 2026'
      ]
    },
    // 6 LB - CONFIRMED: Greco-Taylor
    {
      name:'Christian Greco-Taylor',pos:'Left Back',short:'LB',jersey:'15',confirmed:true,
      club:'Pacific FC - CPL',
      ig:'https://www.instagram.com/cgrecotaylorr/',igHandle:'@cgrecotaylorr',initials:'CGT',
      photo:IMG.greco, alt:'Christian Greco-Taylor headshot in a purple and black Pacific FC kit',
      season:{comp:'CPL 2026',apps:23,starts:18,mins:1695,g:0,a:2},
      stats:[{l:'Defending',v:83},{l:'Pace',v:81},{l:'Stamina',v:85},{l:'Passing',v:76},{l:'Tackling',v:82}],
      accolades:[
        '⭐ 18 CPL starts and 2 assists in 2026',
        '🇨🇦 Canada U-20 International',
        '📺 Featured in the CPL Next Gen series',
        '🍁 From Calgary, Alberta'
      ]
    },
    // 7 CB - CONFIRMED: Matteo Campagna
    {
      name:'Matteo Campagna',pos:'Centre Back',short:'CB',jersey:'5',confirmed:true,agency:'Rabonasports',
      club:'Vancouver FC - CPL',
      ig:'https://www.instagram.com/matteocampagna1/',igHandle:'@matteocampagna1',initials:'MC',
      photo:IMG.campagna, alt:'Matteo Campagna headshot in a black Vancouver FC kit',
      season:{comp:'CPL 2026',apps:26,starts:26,mins:2340,g:2,a:0},
      stats:[{l:'Aerial',v:85},{l:'Tackling',v:83},{l:'Positioning',v:84},{l:'Strength',v:87},{l:'Distribution',v:76}],
      accolades:[
        '🏆 CPL Team of the Week - Weeks 12, 13 and 14 (2026)',
        '⭐ Ever-present: 26 CPL starts, 2 goals, 3 clean sheets',
        '🇨🇦 Canada U-20 International (2022 CONCACAF U-20 Champ.)',
        '🌍 Former Vancouver Whitecaps MLS Homegrown player'
      ]
    },
    // 8 CB - CONFIRMED: Marko Stojadinovic
    {
      name:'Marko Stojadinovic',pos:'Centre Back / Midfielder',short:'CB',jersey:'6',confirmed:true,
      club:'Toronto FC II - MLS Next Pro',
      ig:'',igHandle:'',initials:'MS',photo:'',
      season:{comp:'MLS Next Pro 2026',apps:16,starts:15,mins:1386,g:0,a:2},
      extra:'Made 5 appearances for Atlético Ottawa before the club and player parted ways on 20 May 2026.',
      note:'21-year-old from Caledon, Ontario. Versatile: centre-back, full-back or defensive midfield. Back at Toronto FC II since May 2026.',
      stats:[{l:'Aerial',v:83},{l:'Tackling',v:84},{l:'Positioning',v:82},{l:'Strength',v:83},{l:'Distribution',v:80}],
      accolades:[
        '⭐ 15 MLS Next Pro starts, 2 assists in 2026',
        '🔥 67 earlier appearances for Toronto FC II',
        '🌍 SC Verl U19 (Germany)',
        '🍁 From Caledon, Ontario - TFC Academy',
        '🍁 TNB Starting XI Confirmed'
      ]
    },
    // 9 RB - IN CONTENTION: Thomas LeBeuf
    {
      name:'Thomas LeBeuf',pos:'Right Back',short:'RB',jersey:'3',confirmed:'contention',
      club:'FC Supra du Quebec - CPL',
      ig:'',igHandle:'',initials:'TL',photo:'',
      season:{comp:'CPL 2026',apps:10,starts:7,mins:617,g:0,a:0},
      note:'21-year-old full-back from Quebec. A natural left-back, deployed on the right in the XI. Part of FC Supra\'s first CPL season.',
      stats:[{l:'Pace',v:84},{l:'Defending',v:81},{l:'Stamina',v:86},{l:'Crossing',v:80},{l:'Tackling',v:79}],
      accolades:[
        '🏆 CPL Team of the Week - Week 16 (2026)',
        '⭐ FC Supra du Quebec - contract through 2027',
        '🎓 UNLV NCAA Division 1',
        '🔥 Forge FC CPL trial'
      ]
    },
    // 10 GK - CONFIRMED: Pavela
    {
      name:'Ivan Pavela',pos:'Goalkeeper',short:'GK',jersey:'12',confirmed:true,agency:'Rabonasports',
      club:'Inter Toronto FC - CPL',
      ig:'https://www.instagram.com/ivanpavela/',igHandle:'@ivanpavela',initials:'IP',
      photo:IMG.pavela, alt:'Ivan Pavela headshot in a yellow Inter Toronto FC goalkeeper kit',
      season:{comp:'CPL 2026',apps:6,starts:6,mins:540,g:0,a:0,saves:27,ga:15,cs:0},
      stats:[{l:'Reflexes',v:84},{l:'Positioning',v:82},{l:'Aerial',v:85},{l:'Distribution',v:78},{l:'Command',v:80}],
      accolades:[
        '🏆 CPL Team of the Week - Week 18 (2026)',
        '🧤 27 CPL saves in 2026',
        '⭐ CPL Next Gen Class of 2025',
        '🇨🇦 Canada U-20 International (2024)',
        '🌍 HNK Hajduk Split U19 - NK Lokomotiva Zagreb (Croatia)',
        '🌍 Puskas Akademia U19 (Hungary)'
      ]
    }
  ];
