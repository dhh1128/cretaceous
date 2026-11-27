-- Pandoc filter: the assembled book -> PDF. The print-shaped sibling of kdp.lua.
-- Adapted from ~/code/me/viking/build (kelun), 2026-11-25.
--
-- Same reading of the source, with LaTeX where that file emits OOXML:
--   <hr>            -> \clearpage (front-matter section separator)
--   <br>            -> real line break
--   # Drift         -> centered title block; the byline after it -> centered author
--   ## N            -> unnumbered \chapter, so the bare numeral IS the heading.
--                      A numbered one would set "Chapter 1" above a title of "1".
--   § on its own    -> centered scene break, and the paragraph after it runs
--                      flush left, as after a chapter head
--   ![alt](img){.illustration} alone in a paragraph
--                   -> a float page of its own, the image scaled to the text
--                      block. LaTeX puts it on the next page it can fill, so the
--                      prose is never split around it.

local CLEARPAGE = pandoc.RawBlock('latex', '\\clearpage')

-- Marker text is matched again in Blocks, so keep it distinctive.
local SCENE_BREAK =
  '\\begin{center}\\vspace{0.6\\baselineskip}§\\vspace{0.6\\baselineskip}\\end{center}% scene-break'

-- Render inlines through pandoc so LaTeX specials are escaped and any emphasis
-- in a title or byline survives.
local function to_latex(inlines)
  return pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'latex'):gsub('%s+$', '')
end

-- Track the title/byline handoff across block traversals.
local title_seen = false
local byline_done = false
local first_chapter_done = false
local series_seen = false

function RawBlock(el)
  if el.format:match('html') and el.text:match('^%s*<hr%s*/?>%s*$') then
    return CLEARPAGE
  end
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
  return blk.t == 'RawBlock' and blk.format == 'latex'
    and blk.text:match('scene%-break')
end

-- The chapter label: a paragraph that is one italic run, right after the
-- chapter heading or after the epigraph that follows it.
local function is_label(blk, prev)
  return blk.t == 'Para' and #blk.content == 1 and blk.content[1].t == 'Emph'
    and prev and (prev.t == 'Header' or prev.t == 'BlockQuote'
      or (prev.t == 'RawBlock' and prev.text:match('epigraph%-end')))
end

-- LaTeX indents every paragraph but the first after a heading. A paragraph
-- opening a new scene should read the same way, so kill its indent too.
function Blocks(blocks)
  local out = pandoc.Blocks({})
  for i, blk in ipairs(blocks) do
    if is_label(blk, blocks[i - 1]) then
      blk = pandoc.RawBlock('latex', '\\vspace{12pt}\\begin{center}' .. to_latex(blk.content)
        .. '\\end{center}\\vspace{0.5\\baselineskip}')
    elseif blk.t == 'Para' and i > 1 and (is_scene_break(blocks[i - 1])
        or is_label(blocks[i - 1], blocks[i - 2])) then
      blk.content:insert(1, pandoc.RawInline('latex', '\\noindent '))
    end
    out:insert(blk)
  end
  return out
end

function Header(el)
  if el.level == 1 then
    title_seen = true
    -- Front matter carries no page numbers; the count restarts at chapter 1.
    local lead = series_seen and '' or '\\pagestyle{empty}\\vspace*{2in}'
    return pandoc.RawBlock('latex',
      lead .. '\\begin{center}{\\Huge '
      .. to_latex(el.content) .. '}\\end{center}')
  end
  if el.level == 2 then
    el.level = 1
    el.classes:insert('unnumbered')
    if not first_chapter_done then
      first_chapter_done = true
      return {
        -- Chapter 1 opens on a right-hand page, page 1 (Daniel, 2026-11-25).
        pandoc.RawBlock('latex',
          '\\cleardoublepage\\pagestyle{headings}\\setcounter{page}{1}'),
        el,
      }
    end
    return el
  end
end

-- An epigraph is an archival document, so it is set like one: typewriter,
-- ragged right, and without the source's bold.
local function unbold(el)
  return el:walk({ Strong = function(s) return s.content end })
end

function BlockQuote(el)
  local out = pandoc.Blocks({
    pandoc.RawBlock('latex', '\\begin{quote}\\raggedright\\ttfamily\\small'),
  })
  out:extend(unbold(el).content)
  out:insert(pandoc.RawBlock('latex', '\\end{quote}% epigraph-end'))
  return out
end

function Div(el)
  if el.classes:includes('series') then
    series_seen = true
    return pandoc.RawBlock('latex',
      '\\pagestyle{empty}\\vspace*{1.6in}\\begin{center}{\\large\\scshape '
      .. to_latex(pandoc.utils.blocks_to_inlines(el.content))
      .. '}\\end{center}\\vspace{0.8em}')
  end
  if el.classes:includes('dedication') then
    return pandoc.RawBlock('latex',
      '\\vspace*{2in}\\begin{center}\\itshape '
      .. to_latex(pandoc.utils.blocks_to_inlines(el.content)) .. '\\end{center}')
  end
end

local function is_illustration(el)
  return #el.content == 1 and el.content[1].t == 'Image'
    and el.content[1].classes:includes('illustration')
end

function Para(el)
  -- Interior illustration. tectonic runs in a temporary directory, so the path
  -- is made absolute; the alt text is for e-readers and has no place in print.
  if is_illustration(el) then
    local src = el.content[1].src
    if not src:match('^/') then
      src = pandoc.system.get_working_directory() .. '/' .. src
    end
    return pandoc.RawBlock('latex',
      '\\begin{figure}[p]\\centering\\includegraphics[width=\\textwidth,height=\\textheight,keepaspectratio]{'
      .. src .. '}\\end{figure}')
  end
  -- Scene break: a paragraph that is nothing but the section mark.
  if #el.content == 1 and el.content[1].t == 'Str' and el.content[1].text == '§' then
    return pandoc.RawBlock('latex', SCENE_BREAK)
  end
  -- The byline sits immediately after the title.
  if title_seen and not byline_done then
    byline_done = true
    return pandoc.RawBlock('latex',
      '\\vspace{1.5em}\\begin{center}{\\Large ' .. to_latex(el.content) .. '}\\end{center}')
  end
end
