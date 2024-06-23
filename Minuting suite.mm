<map version="freeplane 1.9.13">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="Minuting suite" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1718656605281" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" associatedTemplateLocation="template:/standard-1.6.mm" show_note_icons="true" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent CONTENT-TYPE="plain/auto" TYPE="DETAILS"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#afd3f7" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#afd3f7"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="6" RULE="ON_BRANCH_CREATION"/>
<node POSITION="right" ID="ID_352138102" CREATED="1718656516571" MODIFIED="1718657778301"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>Framework</b>
    </p>
  </body>
</html>
</richcontent>
<edge COLOR="#7c0000"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      The idea here is to get an MVP of a framework that does the following:
    </p>
    <p>
      
    </p>
    <p>
      User registers ID with contract through phone app for free
    </p>
    <p>
      
    </p>
    <p>
      User gets positive feedback from validators, app is initialized
    </p>
    <p>
      
    </p>
    <p>
      User can then gather time-subsidies or partake in the TWF'd* niche and gather subsidies from that with activity time.
    </p>
    <p>
      
    </p>
    <p>
      User has admin controls that allow changing reward address and backing up / restoring keys as needed.
    </p>
    <p>
      
    </p>
    <p>
      *TWF = Two-way funded
    </p>
  </body>
</html></richcontent>
<node ID="ID_1786542041" CREATED="1718655781055" MODIFIED="1718656623316" HGAP_QUANTITY="14 pt" VSHIFT_QUANTITY="-21.75 pt"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b><u>Phone app</u></b>
    </p>
  </body>
</html>
</richcontent>
<richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      MVP: Flask server in a Trust wallet with the backend connected to through Trust wallet browser
    </p>
    <p>
      
    </p>
    <p>
      Later on: Cordova wrapper with html5 / js frontend; some keys / variables saved
    </p>
  </body>
</html></richcontent>
<node TEXT="ID onboarding facilities" ID="ID_186269483" CREATED="1718655838878" MODIFIED="1718658591008"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Need sandbox environment to vet the service
    </p>
    <p>
      
    </p>
    <p>
      Basically it's clientsided to get a token and apply to the blockchain with
    </p>
    <p>
      only pay upon successful token (running tab needs adminship)
    </p>
    <p>
      
    </p>
    <p>
      Apply for free via IRC<br/><br/><br/>ID onboarding field is a simple string, validators convene to check validity
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="DEX crypto offramp" ID="ID_407673750" CREATED="1718656115394" MODIFIED="1718656316935"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Go with Pancakeswap or Icecreamswap
    </p>
    <p>
      
    </p>
    <p>
      Just need a place to trade tokens with other crypto
    </p>
    <p>
      
    </p>
    <p>
      Then suggest fiat exchange cash offramp paths
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="Cash offramp/onramp" ID="ID_1209123178" CREATED="1718656146850" MODIFIED="1718656270014"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Big licensing need for central approach, not doing this (avoid centralization in general)
    </p>
    <p>
      
    </p>
    <p>
      better to find common exchange fiat onramps / offramps
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="Blockchain backend" ID="ID_630772089" CREATED="1718656581719" MODIFIED="1718657423891">
<node TEXT="EVM blockchain contracts" ID="ID_635051953" CREATED="1718656628905" MODIFIED="1718657153469">
<node TEXT="1. LamportPassword base" ID="ID_1722241877" CREATED="1718657158575" MODIFIED="1718657171929"/>
<node TEXT="2. AnonID database" ID="ID_1492220192" CREATED="1718657174479" MODIFIED="1718657183407">
<node TEXT="AnonID onboarding contract" ID="ID_431688550" CREATED="1718658630677" MODIFIED="1718658645676">
<node TEXT="Validator convention" ID="ID_1406694363" CREATED="1718658648065" MODIFIED="1718658660572"/>
</node>
</node>
<node TEXT="3. PlayerDatabase" ID="ID_471728809" CREATED="1718657188346" MODIFIED="1718657258326"/>
<node TEXT="4. Game validator logic" ID="ID_1167019610" CREATED="1718657260717" MODIFIED="1718657269944">
<node TEXT="Game validator convention" ID="ID_986062866" CREATED="1718658619820" MODIFIED="1718658626145"/>
</node>
<node TEXT="5. Onboarding contract" ID="ID_606290664" CREATED="1718657276342" MODIFIED="1718657283737">
<node TEXT="Validator convention&#xa;(Game validators repurposed)" ID="ID_324623784" CREATED="1718658606737" MODIFIED="1718658752736"/>
</node>
<node TEXT="6. Forum" ID="ID_366782913" CREATED="1718657286242" MODIFIED="1718657291453"/>
<node TEXT="DAO stuff" ID="ID_1782944288" CREATED="1718657297370" MODIFIED="1718657304717"/>
<node TEXT="Brownie scripts" ID="ID_167724543" CREATED="1718657508224" MODIFIED="1718657580531"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      deploy.py and interaction.py are the crux of the python-based DEX swap demonstration
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="Javascript contract&#xa;deployment env" ID="ID_1624530418" CREATED="1718657356968" MODIFIED="1718657489832" HGAP_QUANTITY="8.75 pt" VSHIFT_QUANTITY="24.75 pt"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Allows user to deploy accurate bytecode for fiddling with Uniswapv2 functions
    </p>
    <p>
      
    </p>
    <p>
      Doing it in python for some reason leads to arcane errors
    </p>
    <p>
      
    </p>
    <p>
      That said once deployed this way you can work on the swaps in python properly
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="TDL" ID="ID_802491409" CREATED="1718657881272" MODIFIED="1718673411055">
<node TEXT="Get a test phone together" ID="ID_588243490" CREATED="1718657888659" MODIFIED="1718673407407"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      will do 18th (cap card comes morning)
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="Get MVP going" ID="ID_804519181" CREATED="1718666301547" MODIFIED="1718673492068"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      fiddle around with scripts get something to piece together in your mind
    </p>
  </body>
</html></richcontent>
</node>
</node>
</node>
</node>
</map>
