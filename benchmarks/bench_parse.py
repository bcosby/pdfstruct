import sys, time, tracemalloc
from pdfstruct import PDFParser

p = sys.argv[1]
tracemalloc.start()
t0=time.perf_counter(); doc=PDFParser(p).parse(); t1=time.perf_counter()
t2=time.perf_counter(); _=doc.to_dict()['pages']; t3=time.perf_counter()
t4=time.perf_counter(); _=doc.to_json(); t5=time.perf_counter()
_, peak = tracemalloc.get_traced_memory()
d=doc.to_dict()
print(f"file: {p}")
print(f"size: {d['file']['size']/1024:.1f} KB")
print(f"objects: {len(d['objects'])}")
print(f"pages: {len(d['pages'])}")
print(f"streams: {sum(1 for o in d['objects'].values() if o.get('type')=='stream')}")
print(f"parse_ms: {(t1-t0)*1000:.2f}")
print(f"text_ms: {(t3-t2)*1000:.2f}")
print(f"json_ms: {(t5-t4)*1000:.2f}")
print(f"peak_memory_kb: {peak/1024:.0f}")
