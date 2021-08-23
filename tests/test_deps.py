import pytest
from htmltools import *

def expect_resolved_deps(input, output):
  actual = tag_list(*input).get_dependencies()
  assert actual == output

def expect_html_deps(x, html_, deps):
  assert str(x.get_html_string()) == html_
  assert x.get_dependencies() == deps

def test_dep_resolution():
  a1_1 = html_dependency("a", "1.1", {"href":"/"})
  a1_2 = html_dependency("a", "1.2", {"href":"/"})
  a1_2_1 = html_dependency("a", "1.2.1", {"href":"/"})
  b1_0_0 = html_dependency("b", "1.0.0", {"href":"/"})
  b1_0_1 = html_dependency("b", "1.0.1", {"href":"/"})
  c1_0 = html_dependency("c", "1.0", {"href":"/"})
  expect_resolved_deps(
    [a1_1, b1_0_0, b1_0_1, a1_2, a1_2_1, b1_0_0, b1_0_1, c1_0],
    [a1_2_1, b1_0_1, c1_0]
  )

def test_inline_deps():
  # Test out renderTags and findDependencies when tags are inline
  a1_1 = html_dependency("a", "1.1", {"href":"/"})
  a1_2 = html_dependency("a", "1.2", {"href":"/"})
  # tagLists ----------------------------------------------------------
  expect_html_deps(
    tag_list(a1_1, div("foo"), "bar"), 
    "<div>foo</div>\nbar", [a1_1]
  )
  expect_html_deps(
    tag_list(a1_1, div("foo"), a1_2, "bar"), 
    "<div>foo</div>\nbar", [a1_2]
  )
  # tags with children ------------------------------------------------
  expect_html_deps(
    div(a1_1, div("foo"), "bar"), 
    "<div>\n  <div>foo</div>\n  bar\n</div>", [a1_1]
  )
  # Passing normal lists to tagLists and tag functions  ---------------
  expect_html_deps(
    tag_list([a1_1, div("foo")], "bar"), 
    "<div>foo</div>\nbar", [a1_1]
  )
  expect_html_deps(
    div([a1_1, div("foo")], "bar"), 
    "<div>\n  <div>foo</div>\n  bar\n</div>", [a1_1]
  )

def test_append_deps():
  a1_1 = html_dependency("a", "1.1", {"href":"/"})
  a1_2 = html_dependency("a", "1.2", {"href":"/"})
  b1_2 = html_dependency("b", "1.0", {"href":"/"})
  x = div(a1_1, b1_2)
  x.append_children(a1_2)
  expect_html_deps(x, "<div></div>", [a1_2, b1_2])
  x = div(a1_1)
  x.append_children([a1_2, b1_2])
  expect_html_deps(x, "<div></div>", [a1_2, b1_2])
  x = div()
  x.append_children([a1_1, b1_2])
  x.append_children(a1_2)
  expect_html_deps(x, "<div></div>", [a1_2, b1_2])


def test_script_input():
  def fake_dep(**kwargs):
    return html_dependency("a", "1.0", ".", **kwargs)
  dep1 = fake_dep(script = "js/foo bar.js", stylesheet = "css/bar foo.css")
  dep2 = fake_dep(script = ["js/foo bar.js"], stylesheet = ["css/bar foo.css"])
  dep3 = fake_dep(script = [{"src": "js/foo bar.js"}], stylesheet = [{"href": "css/bar foo.css"}])
  assert dep1 == dep2 == dep3
  assert str(dep1.as_tags()) == '<link href="css/bar%20foo.css" rel="stylesheet"/>\n<script src="js/foo%20bar.js"></script>'
  # Make sure repeated calls to as_html() repeatedly encode
  assert str(dep1.as_tags()) == '<link href="css/bar%20foo.css" rel="stylesheet"/>\n<script src="js/foo%20bar.js"></script>'

#def test_nested_deps():
#    src = "https://cdn.com/libs/p1/0.1"
#    nm = "p1.js"
#    d1 = html_dependency(
#      "p1", "0.1", src = {"href": src),
#      script = {"src": nm)
#    )
#    deps1 = [
#      d1,
#      html_dependency(
#        "p1", "0.2", src = {"href": src),
#        script = nm
#      ),
#      html_dependency(
#        "p1", "0.3", src = {"href": src),
#        script = [{"src": nm))
#      )
#    )
#    out = renderDependencies(deps1)
#    deps2 = [d1, d1, d1]
#    expect_length(unique(un[strsplit(out, "\n"))), 1)
#    expect_equal(renderDependencies(deps1), renderDependencies(deps2))
#    nm2 = "p1-0.1.js"
#    deps3 = [
#      html_dependency(
#        "p1", "0.1", src = {"href": src),
#        script = c(nm, nm2)
#      )
#    )
#    out = renderDependencies(deps3)
#    src_urls = c(
#      file.path(src, nm),
#      file.path(src, nm2)
#      )
#    expect = paste(
#      '<script src="', src_urls[[1]],'"></script>\n',
#      '<script src="', src_urls[[2]],'"></script>',
#      sep = "")
#    expect_equal(!!as.character(out), !!expect)
#    deps4 = [
#      html_dependency(
#        "p1", "0.1", src = {"href": src),
#        script = [{"src": nm, "integrity": "hash"), nm2)
#      )
#    )
#    out = renderDependencies(deps4)
#    expect = paste(
#      '<script src="', src_urls[[1]], '" integrity="hash"></script>\n',
#      '<script src="', src_urls[[2]], '"></script>',
#      sep = "")
#    expect_equal(!!as.character(out), !!expect)
#

#
#def test_dep_rendering():
#  src1 = "https://cdn.com/libs/p1/0.1/"
#  src2 = "https://cdn/libs/p2/0.2/"
#  deps = [
#    html_dependency(
#      name = "p1",
#      version = "0.1",
#      src = {"href": src1},
#      script = [
#        src = "p1.min.js",
#        "integrity": "longhash",
#        crossorigin = "anonymous",
#        defer = NA
#      )
#    ),
#    html_dependency(
#      "p2", version = "0.2",
#      src = {"href": src2),
#      script = "p2.min.js"
#    )
#  )
#  expect1 = paste(
#    '<script src="', src1, 'p1.min.js','" ',
#    'integrity="longhash" ',
#    'crossorigin="anonymous" defer></script>',
#    sep = ''
#  )
#  expect2 = paste(
#    '<script src="', src2, 'p2.min.js','"></script>',
#    sep = ''
#  )
#  expect = paste(expect1, expect2, sep = '\n')
#  class(expect) = c("html", "character")
#  actual = renderDependencies(deps)
#  expect_equal(!!strsplit(actual, "\n"), !!strsplit(expect, "\n"))
#
