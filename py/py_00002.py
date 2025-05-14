# Comment: Read all the metadata from a file
    def read(self, pathname, format="grib"):
        
        ds = arki.DatasetReader({
            "format": format,
            "name": os.path.basename(pathname),
            "path": pathname,
            "type": "file",
        })

        res = []
        def store_md(md):
            nonlocal res
            res.append(md)
        ds.query_data(on_metadata=store_md)

        return res



