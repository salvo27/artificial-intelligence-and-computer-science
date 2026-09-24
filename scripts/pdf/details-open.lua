-- Print the content of <details> blocks (solutions to exercises),
-- which would otherwise stay collapsed in the PDF.
function RawBlock(el)
  if el.format == "html" then
    el.text = el.text:gsub("<details>", "<details open>")
    return el
  end
end
