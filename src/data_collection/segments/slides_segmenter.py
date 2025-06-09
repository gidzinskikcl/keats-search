from data_collection.segments import segment, segmenter


class SlidesSegmenter(segmenter.Segmenter):

    def segment(self, data: dict[str, str]) -> list[segment.Segment]:
        pages = data["pages"]
        result = []
        for page_nr_str, content in pages.items():
            try:
                page_nr = int(page_nr_str)
            except ValueError:
                page_nr = 0  # fallback if the key is non-numeric

            sgmnt = segment.Segment(nr=page_nr, content=content.strip())
            result.append(sgmnt)
        return result