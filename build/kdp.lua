-- Pandoc filter: the assembled book -> DOCX shaped for Kindle Create import.
-- Adapted from ~/code/me/viking/build (kelun), 2026-11-25.
--
-- What it does:
--   <hr>            -> hard page break (front-matter section separator)
--   <br>            -> real line break (pandoc drops raw HTML in the docx writer)
--   # Drift         -> "Title" styled paragraph; the byline after it -> "Author"
--   ## N            -> Heading 1 (Kindle Create finds chapters by Heading 1; the
--                      page break comes from the style's pageBreakBefore, so no
--                      empty break paragraph is emitted here)
--   § on its own    -> "Scene Break" styled paragraph (centered)
--   ::: series      -> "Series" styled line above the title (in an epub, folded
--                      into the title heading, which is kept out of the TOC)
--   ::: dedication  -> "Dedication" styled paragraph, centered
--   *label* line    -> the chapter's day/POV/place label, centered; the prose
--                      after it opens flush left, as after a chapter head

local EPUB = FORMAT:match('epub') ~= nil

local PAGE_BREAK = EPUB
  and pandoc.RawBlock('html', '<div class="page-break"></div>')
  or pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

-- The docx writer reads custom-style; an epub needs a class its stylesheet
-- (build/epub.css) can match, so the same name becomes a class there:
-- "Scene Break" -> scene-break.

local function styled(style, blocks)
  if EPUB then
    local cls = style:lower():gsub(' ', '-')
    return pandoc.Div(blocks, pandoc.Attr('', { cls }, {}))
  end
  return pandoc.Div(blocks, pandoc.Attr('', {}, { ['custom-style'] = style }))
end

local function has_style(blk, style)
  if blk.t ~= 'Div' then return false end
  if EPUB then return blk.classes:includes((style:lower():gsub(' ', '-'))) end
  return blk.attributes['custom-style'] == style
end

-- Track the title/byline handoff across block traversals.
local title_seen = false
local byline_done = false

function RawBlock(el)
  if el.format:match('html') and el.text:match('^%s*<hr%s*/?>%s*$') then
    return PAGE_BREAK
  end
end

local function is_page_break(blk)
  return blk.t == 'RawBlock'
    and (blk.text:match('w:type="page"') or blk.text:match('page%-break'))
end

-- <br> -> LineBreak, and swallow the space the source newline leaves behind.
function Inlines(inlines)
  local out = pandoc.Inlines({})
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if el.t == 'RawInline' and el.format:match('html')
      and el.text:match('^%s*<br%s*/?>%s*$') then
      out:insert(pandoc.LineBreak())
      local nxt = inlines[i + 1]
      if nxt and (nxt.t == 'Space' or nxt.t == 'SoftBreak') then i = i + 1 end
    else
      out:insert(el)
    end
    i = i + 1
  end
  return out
end

local function is_scene_break(blk)
  return has_style(blk, 'Scene Break')
end

-- The chapter label: a paragraph that is one italic run, right after the
-- chapter heading or after the epigraph that follows it.
local function is_label(blk, prev)
  return blk.t == 'Para' and #blk.content == 1 and blk.content[1].t == 'Emph'
    and prev and (prev.t == 'Header' or prev.t == 'BlockQuote')
end

-- Two passes over each block list:
--   * drop a front-matter <hr> that sits right before a chapter heading — it
--     would double up with the heading style's own page break, leaving a blank
--     page;
--   * set the paragraph after a scene break flush left, as after a chapter head.
function Blocks(blocks)
  local out = pandoc.Blocks({})
  for i, blk in ipairs(blocks) do
    local nxt = blocks[i + 1]
    if is_page_break(blk) and nxt and nxt.t == 'Header' and nxt.level == 1 then
      -- skip
    elseif EPUB and has_style(blk, 'Series') and nxt and nxt.t == 'Header' then
      -- Content before the first heading becomes a chunk of its own, with a
      -- heading pandoc invents, so the series line rides inside the title.
      local series = pandoc.utils.blocks_to_inlines(blk.content)
      local inl = pandoc.Inlines({ pandoc.Span(series, pandoc.Attr('', { 'series' })),
        pandoc.LineBreak() })
      inl:extend(nxt.content)
      nxt.content = inl
    elseif is_label(blk, blocks[i - 1]) then
      out:insert(styled('Chapter Label', { blk }))
    elseif blk.t == 'Para' and i > 1 and (is_scene_break(blocks[i - 1])
        or is_label(blocks[i - 1], blocks[i - 2])) then
      out:insert(styled('First Paragraph', { blk }))
    else
      out:insert(blk)
    end
  end
  return out
end

function Header(el)
  if el.level == 1 then
    title_seen = true
    -- In an epub the title stays a heading, or pandoc invents one for the
    -- unheaded front-matter chunk and the title shows twice.
    if EPUB then
      el.classes:insert('title')
      el.classes:insert('unnumbered')
      el.classes:insert('unlisted')
      return el
    end
    return styled('Title', { pandoc.Para(el.content) })
  end
  if el.level == 2 then
    el.level = 1
    return el
  end
end

function Div(el)
  if el.classes:includes('series') then
    return styled('Series', el.content)
  end
  if el.classes:includes('dedication') then
    return styled('Dedication', el.content)
  end
end

function Para(el)
  -- Scene break: a paragraph that is nothing but the section mark.
  if #el.content == 1 and el.content[1].t == 'Str' and el.content[1].text == '§' then
    return styled('Scene Break', { el })
  end
  -- The byline sits immediately after the title.
  if title_seen and not byline_done then
    byline_done = true
    return styled('Author', { el })
  end
end
