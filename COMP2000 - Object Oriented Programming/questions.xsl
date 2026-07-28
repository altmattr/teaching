<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:key name="q-by-cat"
    match="question[not(@type='category')]"
    use="generate-id(preceding-sibling::question[@type='category'][1])"/>

  <xsl:template match="/quiz">
    <xsl:variable name="bank-name">
      <xsl:choose>
        <xsl:when test="question[@type='category' and contains(category/text, '/RATS/')]">RATS</xsl:when>
        <xsl:when test="question[@type='category' and contains(category/text, '/Practice Exam/')]">Practice Exam</xsl:when>
        <xsl:when test="question[@type='category' and contains(category/text, '/Final Exam/')]">Final Exam</xsl:when>
        <xsl:otherwise>Question Bank</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <html>
      <head>
        <meta charset="UTF-8"/>
        <title><xsl:value-of select="$bank-name"/> Question Bank</title>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="crossorigin"/>
        <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }

          body {
            font-family: 'Fira Sans', sans-serif;
            color: rgb(56,58,54);
            background: #fafaf9;
          }

          /* ===== radio inputs (hidden) ===== */
          .w-rad { display: none; }

          /* ===== header ===== */
          .header {
            max-width: 960px;
            margin: 0 auto;
            padding: 2em 2em 0 2em;
          }
          .header h1 {
            color: rgb(109,41,49);
            font-weight: 700;
            font-size: 2em;
            margin-bottom: 0.2em;
          }
          .header .subtitle {
            font-weight: 400;
            font-size: 0.95em;
            opacity: 0.7;
            margin-bottom: 1em;
          }

          /* ===== floating tab bar ===== */
          .tab-nav {
            position: sticky;
            top: 0;
            z-index: 10;
            background: white;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0;
            padding: 0 0.5em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
          }
          .tab-nav label {
            display: inline-block;
            padding: 0.7em 1em;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85em;
            color: rgb(56,58,54);
            border-bottom: 2px solid transparent;
            transition: border-color 0.15s, color 0.15s;
            white-space: nowrap;
          }
          .tab-nav label:hover {
            color: rgb(188,71,0);
          }

          /* ===== tab panels ===== */
          .tab-panel {
            display: none;
            max-width: 960px;
            margin: 0 auto;
            padding: 1.5em 2em 3em 2em;
          }

          .tab-panel .panel-heading {
            font-weight: 600;
            font-size: 1.15em;
            color: rgb(56,58,54);
            margin-bottom: 1em;
            padding-bottom: 0.4em;
            border-bottom: 2px solid rgb(188,71,0);
          }

          /* ===== question cards ===== */
          .question {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1.2em 1.5em;
            margin: 0.8em 0;
            transition: border-color 0.15s;
          }
          .question:hover {
            border-color: rgb(188,71,0);
          }

          .q-header {
            display: flex;
            align-items: center;
            gap: 0.6em;
            margin-bottom: 0.8em;
          }
          .q-name {
            font-weight: 600;
            color: rgb(56,58,54);
            font-size: 1em;
          }
          .q-badge {
            display: inline-block;
            font-size: 0.7em;
            font-weight: 600;
            padding: 0.2em 0.6em;
            border-radius: 3px;
            color: white;
            text-transform: uppercase;
            letter-spacing: 0.03em;
          }
          .q-badge.single { background: rgb(25,33,139); }
          .q-badge.multi  { background: rgb(188,71,0); }
          .q-badge.match  { background: rgb(109,41,49); }

          .q-text {
            margin-bottom: 0.8em;
            line-height: 1.5;
          }
          .q-text p { margin: 0.3em 0; }
          .q-text pre {
            background: #f5f5f4;
            padding: 0.5em;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9em;
          }

          .answers { list-style: none; padding: 0; }
          .answers li {
            padding: 0.4em 0.6em;
            margin: 0.2em 0;
            border-radius: 4px;
            border: 1px solid transparent;
          }
          .answers li.correct {
            background: #e8f5e9;
            border-color: #a5d6a7;
          }
          .answers li .marker {
            font-weight: 700;
            color: rgb(152,41,50);
            margin-right: 0.4em;
          }

          .match-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5em;
          }
          .match-table th {
            text-align: left;
            padding: 0.5em 0.8em;
            background: #f0f0ee;
            font-weight: 600;
            font-size: 0.85em;
            border: 1px solid #ddd;
          }
          .match-table td {
            padding: 0.5em 0.8em;
            border: 1px solid #ddd;
            vertical-align: top;
            line-height: 1.4;
          }
          .match-table tr:nth-child(even) td {
            background: #f8f8f7;
          }

          .feedback {
            margin-top: 0.8em;
            padding: 0.6em 0.8em;
            background: #fff8e1;
            border-radius: 4px;
            font-size: 0.9em;
            border-left: 3px solid rgb(188,71,0);
          }
          .feedback p { margin: 0.2em 0; }

          <xsl:for-each select="question[@type='category']">
            <xsl:variable name="id" select="concat('w-', position())"/>
            <xsl:text>#</xsl:text><xsl:value-of select="$id"/><xsl:text>:checked ~ .tp-</xsl:text><xsl:value-of select="$id"/><xsl:text> { display: block; }
</xsl:text>
          </xsl:for-each>

          <xsl:for-each select="question[@type='category']">
            <xsl:variable name="id" select="concat('w-', position())"/>
            <xsl:text>#</xsl:text><xsl:value-of select="$id"/><xsl:text>:checked ~ .tab-nav label[for="</xsl:text><xsl:value-of select="$id"/><xsl:text>"] { border-bottom-color: rgb(188,71,0); color: rgb(188,71,0); }
</xsl:text>
          </xsl:for-each>
        </style>
      </head>
      <body>

        <!-- ===== radio inputs ===== -->
        <xsl:for-each select="question[@type='category']">
          <xsl:variable name="id" select="concat('w-', position())"/>
          <input type="radio" name="w" class="w-rad">
            <xsl:attribute name="id"><xsl:value-of select="$id"/></xsl:attribute>
            <xsl:if test="position() = 1">
              <xsl:attribute name="checked">checked</xsl:attribute>
            </xsl:if>
          </input>
        </xsl:for-each>

        <!-- ===== header ===== -->
        <div class="header">
          <h1><xsl:value-of select="$bank-name"/> Question Bank</h1>
          <p class="subtitle">
            <xsl:value-of select="count(question[not(@type='category')])"/> questions across
            <xsl:value-of select="count(question[@type='category'])"/> weeks
          </p>
        </div>

        <!-- ===== tab bar ===== -->
        <div class="tab-nav">
          <xsl:for-each select="question[@type='category']">
            <xsl:variable name="id" select="concat('w-', position())"/>
            <label>
              <xsl:attribute name="for"><xsl:value-of select="$id"/></xsl:attribute>
              <xsl:call-template name="week-label">
                <xsl:with-param name="cat" select="category/text"/>
              </xsl:call-template>
              <xsl:text> (</xsl:text>
              <xsl:value-of select="count(key('q-by-cat', generate-id()))"/>
              <xsl:text>)</xsl:text>
            </label>
          </xsl:for-each>
        </div>

        <!-- ===== tab panels ===== -->
        <xsl:for-each select="question[@type='category']">
          <xsl:variable name="id" select="concat('w-', position())"/>
          <xsl:variable name="cat-id" select="generate-id()"/>
          <div class="tab-panel">
            <xsl:attribute name="class">
              <xsl:text>tab-panel tp-</xsl:text>
              <xsl:value-of select="$id"/>
            </xsl:attribute>

            <div class="panel-heading">
              <xsl:call-template name="week-label">
                <xsl:with-param name="cat" select="category/text"/>
              </xsl:call-template>
            </div>

            <xsl:apply-templates select="key('q-by-cat', $cat-id)" mode="q"/>
          </div>
        </xsl:for-each>

      </body>
    </html>
  </xsl:template>

  <!-- ===== extract human-readable week label ===== -->
  <xsl:template name="week-label">
    <xsl:param name="cat"/>
    <xsl:choose>
      <xsl:when test="contains(translate($cat, 'WEEK', 'week'), 'week ')">
        <xsl:text>Week </xsl:text>
        <xsl:value-of select="normalize-space(substring-after(translate($cat, 'WEEK', 'week'), 'week '))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$cat"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ===== render a single question card ===== -->
  <xsl:template match="question" mode="q">
    <div class="question">

      <div class="q-header">
        <span class="q-name"><xsl:value-of select="name/text"/></span>
        <xsl:choose>
          <xsl:when test="@type='multichoice'">
            <xsl:choose>
              <xsl:when test="single='true'">
                <span class="q-badge single">single</span>
              </xsl:when>
              <xsl:otherwise>
                <span class="q-badge multi">multiple</span>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:when test="@type='matching'">
            <span class="q-badge match">matching</span>
          </xsl:when>
          <xsl:otherwise>
            <span class="q-badge"><xsl:value-of select="@type"/></span>
          </xsl:otherwise>
        </xsl:choose>
      </div>

      <div class="q-text">
        <xsl:value-of select="questiontext/text" disable-output-escaping="yes"/>
      </div>

      <xsl:choose>
        <xsl:when test="@type='multichoice'">
          <ul class="answers">
            <xsl:for-each select="answer">
              <li>
                <xsl:if test="starts-with(@fraction, '100')">
                  <xsl:attribute name="class">correct</xsl:attribute>
                </xsl:if>
                <xsl:if test="starts-with(@fraction, '100')">
                  <span class="marker">&#10003;</span>
                </xsl:if>
                <xsl:value-of select="text" disable-output-escaping="yes"/>
              </li>
            </xsl:for-each>
          </ul>
        </xsl:when>

        <xsl:when test="@type='matching'">
          <table class="match-table">
            <tr>
              <th>Term</th>
              <th>Correct match</th>
            </tr>
            <xsl:for-each select="subquestion">
              <tr>
                <td><xsl:value-of select="text" disable-output-escaping="yes"/></td>
                <td><xsl:value-of select="answer/text" disable-output-escaping="yes"/></td>
              </tr>
            </xsl:for-each>
          </table>
        </xsl:when>
      </xsl:choose>

      <xsl:if test="normalize-space(generalfeedback/text)">
        <div class="feedback">
          <xsl:value-of select="generalfeedback/text" disable-output-escaping="yes"/>
        </div>
      </xsl:if>

    </div>
  </xsl:template>

</xsl:stylesheet>
