# Comment: Read all the metadata from a file
    def read(self, pathname, format="grib"):
        
        ds = arki.DatasetReader({
            "format": format,
            "name": os.path.basename(pathname),
            "path": pathname,
            "type": "file",
        })

        return ds.query_summary()



