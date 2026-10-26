# Verify generated publication routes, links, metadata and syndication.
require 'cgi'
require 'json'
require 'pathname'
require 'rexml/document'
require 'uri'

root = Pathname.new(ARGV.fetch(0, '_site')).expand_path
origin = 'https://anuragsarkar97.github.io'
errors = []
files = Dir[root.join('**/*.html')]
abort 'Build the site first.' if files.empty?
files.each do |file|
  html = File.read(file)
  route = '/' + Pathname.new(file).relative_path_from(root).to_s.sub(/index\.html$/, '')
  # The independent drawing app has its own markup and external assets.
  unless route == '/excalidraw/'
    errors << "#{route}: expected one H1" unless html.scan(/<h1\b/i).size == 1
    errors << "#{route}: missing main landmark" unless html.include?('<main ')
    errors << "#{route}: missing canonical" unless html.include?(%(<link rel="canonical" href="#{origin}#{route}">))
    errors << "#{route}: missing description" unless html.match?(/<meta name="description" content="[^"]+">/)
  end
  html.scan(/(?:href|src)="([^"]+)"/).flatten.each do |raw|
    href = CGI.unescapeHTML(raw)
    next if href.start_with?('mailto:', 'data:', 'javascript:', '//')
    begin
      uri = URI.join(origin + route, href)
      next unless uri.host == URI(origin).host
      target = root.join(URI::DEFAULT_PARSER.unescape(uri.path).delete_prefix('/'))
      target = target.join('index.html') if target.directory?
      unless target.file?
        errors << "#{route}: missing #{href}"
        next
      end
      if uri.fragment && !uri.fragment.empty? && target.extname == '.html'
        fragment = URI::DEFAULT_PARSER.unescape(uri.fragment)
        errors << "#{route}: missing anchor #{href}" unless File.read(target).include?(%(id="#{fragment}"))
      end
    rescue URI::InvalidURIError => e
      errors << "#{route}: invalid URL #{href}: #{e.message}"
    end
  end
  html.scan(/<script type="application\/ld\+json">(.*?)<\/script>/m).each do |match|
    data = JSON.parse(match.first)
    errors << "#{route}: incorrect article URL" unless data['mainEntityOfPage'] == origin + route
  end
end
feed = REXML::Document.new(File.read(root.join('atom.xml')).strip)
sitemap = REXML::Document.new(File.read(root.join('sitemap.xml')).strip)
entries = REXML::XPath.match(feed, '//*[local-name()="entry"]')
posts = Dir[root.join('[0-9][0-9][0-9][0-9]/**/index.html')]
errors << 'Feed entry count differs from published articles' unless entries.size == posts.size
urls = REXML::XPath.match(sitemap, '//*[local-name()="loc"]').map(&:text)
entries.each do |entry|
  url = entry.elements['link'].attributes['href']
  errors << "Article missing from sitemap: #{url}" unless urls.include?(url)
  ['index.html', 'blog/index.html'].each do |index|
    path = URI(url).path
    errors << "Article missing from #{index}: #{path}" unless File.read(root.join(index)).include?(%(href="#{path}"))
  end
end
abort errors.join("\n") unless errors.empty?
puts "PASS: #{files.size} HTML pages, #{posts.size} articles, local links and anchors, canonical URLs, metadata, JSON-LD, Atom and sitemap."
