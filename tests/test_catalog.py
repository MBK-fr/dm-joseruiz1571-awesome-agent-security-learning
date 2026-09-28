import copy
from datetime import date
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog import canonical, load, resource_id, validate
from discover import due, feed_items, relevant, select, historical_ids, report, collect, candidate
from build import markdown

class CatalogTests(unittest.TestCase):
    def test_real_catalog(self):
        self.assertGreater(len(validate(load('resources.json'))),20)
    def test_duplicates_ignore_tracking_and_fragment(self):
        a=load('resources.json')[0]; b=copy.deepcopy(a); b['id']='other'; b['url']=a['url']+'?utm_source=mail#section'
        with self.assertRaises(ValueError): validate([a,b])
    def test_url_semantics(self):
        self.assertEqual(canonical('http://github.com/Owner/Repo.git/'), 'https://github.com/owner/repo')
        self.assertNotEqual(resource_id('https://www.youtube.com/watch?v=one'),resource_id('https://www.youtube.com/watch?v=two'))
        self.assertEqual(canonical('https://example.com/p?b=2&a=1&utm_source=x#top'),'https://example.com/p?a=1&b=2')
    def test_dangerous_urls(self):
        for url in ['javascript:alert(1)','https://localhost/a','https://127.0.0.1','https://169.254.169.254/latest','https://user:pass@example.com','https://example.com:8080/a']:
            with self.subTest(url=url),self.assertRaises(ValueError): canonical(url)
    def test_fortnight_across_year_boundary(self):
        anchor=date(2026,9,28)
        for day,expected in [(date(2026,9,28),True),(date(2026,10,5),False),(date(2026,10,12),True),(date(2026,12,28),False),(date(2027,1,4),True)]:
            self.assertEqual(due(day,anchor),expected)
    def test_rss_and_atom(self):
        rss=b'<rss><channel><item><title>Agent security</title><link>https://example.com/a</link><description>Prompt injection</description></item></channel></rss>'
        atom=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Agent safety</title><link rel="self" href="https://example.com/api"/><link href="https://example.com/b"/><summary>Oversight</summary></entry></feed>'
        self.assertEqual(list(feed_items(rss))[0]['url'],'https://example.com/a')
        self.assertEqual(list(feed_items(atom))[0]['url'],'https://example.com/b')
        with self.assertRaises(ValueError): list(feed_items(b'<!DOCTYPE a><rss/>'))
    def test_relevance(self):
        self.assertFalse(relevant('A framework for building agents'))
        self.assertFalse(relevant('A cooking course with recipes'))
        self.assertTrue(relevant('AI agent safety and governance course'))
    def test_selection_dedup_limit_diversity(self):
        a,b,c,d=[{'id':x} for x in 'abcd']
        self.assertEqual(select([[a,b,c],[a,d]],{'b'},3),[a,d,c])
    def test_closed_history(self):
        body='<!-- candidate-id:0123456789abcdef -->'
        with patch('discover.gh',return_value=json.dumps([[{'state':'closed','body':body}],[{'body':None}]])):
            self.assertEqual(historical_ids('a/b'),{'0123456789abcdef'})
    def test_missing_key_fails(self):
        with patch.dict('os.environ',{},clear=True),self.assertRaisesRegex(RuntimeError,'Missing BRAVE'):
            collect(load('discovery.json'),date(2026,9,28))
    def test_candidate_has_no_copied_snippet_or_fake_check(self):
        row=candidate({'title':'Agent security course','url':'https://example.com/a','description':'Secret proprietary snippet'},'Brave Search','query',date(2026,9,28))
        self.assertNotIn('proprietary',row['description']); self.assertIsNone(row['checked_on'])
        self.assertEqual(row['type'],'Courses'); self.assertIn('candidate-id:',report([row],[],False))
    def test_markdown_escaping(self):
        self.assertNotIn('<script>',markdown('<script>alert(1)</script>'))
        self.assertNotIn('[',markdown('[bad](javascript:alert(1))'))

if __name__=='__main__': unittest.main()
