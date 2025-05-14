# Comment: Compute what columns need to be in the output CSV.

It queries DB-All.e once; another query will be needed later to output
data.
    def compute_columns(self, tr, filter):
        
        # Station data indexed by station id
        stations = {}

        # Do one pass over the result set to compute the columns
        columns = [
            ColumnStation(stations),
            ColumnNetwork(),
            ColumnDatetime(),
            ColumnLevel(),
            ColumnTrange(),
            ColumnVar(),
            ColumnValue(),
        ]
        station_var_cols = {}
        attribute_cols = {}
        rowcount = 0
        for row in tr.query_data(filter):
            rowcount += 1
            # Let the columns examine this row
            for c in columns:
                c.add(row)

            # Index station data by ana_id
            id = row["ana_id"]
            stations[id] = [row["lat"], row["lon"], row["ident"]]

            # Load station variables for this station
            if id not in self.station_data:
                query = dict(ana_id=id)
                items = {}
                for record in tr.query_station_data(query):
                    v = record["variable"]
                    items[v.code] = v
                    col = station_var_cols.get(v.code, None)
                    if col is None:
                        station_var_cols[v.code] = col = ColumnStationData(v.code, self.station_data)
                    col.add(v)
                self.station_data[id] = items

            # Load attributes
            attributes = {}
            for key, v in tr.attr_query_data(row["context_id"]).items():
                code = v.code
                attributes[code] = v
                col = attribute_cols.get(code, None)
                if col is None:
                    attribute_cols[code] = col = ColumnAttribute(code, self.attributes)
                col.add(v)
            self.attributes["{},{}".format(row["context_id"], row["var"])] = attributes
        self.rowcount = rowcount

        # Now that we have detailed info, compute the columns

        # Build a list of all candidate columns
        all_columns = []
        all_columns.extend(columns)
        for k, v in sorted(station_var_cols.items()):
            all_columns.append(v)
        for k, v in sorted(attribute_cols.items()):
            all_columns.append(v)

        # Dispatch them between title and csv body
        self.title_columns = []
        self.csv_columns = []
        for col in all_columns:
            if col.is_single_val():
                self.title_columns.append(col)
            else:
                self.csv_columns.append(col)



# Comment: Perform a DB-All.e query using the given query and output the results
in CSV format on the given file object
    def output(self, query, fd):
        
        if sys.version_info[0] >= 3:
            writer = csv.writer(fd, dialect="excel")
        else:
            writer = UnicodeCSVWriter(fd)

        self.compute_columns(self.tr, query)

        # Don't query an empty result set
        if self.rowcount == 0:
            print("Result is empty.", file=sys.stderr)
            return

        row_headers = []
        for c in self.csv_columns:
            row_headers.extend(c.column_labels())

        # Print the title if we have it
        if self.title_columns:
            title = "; ".join(c.title() for c in self.title_columns)
            row = ["" for x in row_headers]
            row[0] = title
            writer.writerow(row)

        # Print the column headers
        writer.writerow(row_headers)

        for rec in self.tr.query_data(query):
            row = []
            for c in self.csv_columns:
                row.extend(c.column_data(rec))
            writer.writerow(row)




# Comment: Hack to work around the csv module being unable to handle unicode rows in
input, and unicode files in output
class UnicodeCSVWriter(object):
    

    class UnicodeFdWrapper(object):
        """
        Wrap an output file descriptor into something that accepts utf8 byte
        strings and forwards unicode
        """
        def __init__(self, outfd):
            self.outfd = outfd

        def write(self, bytestr):
            self.outfd.write(bytestr.decode("utf-8"))

    def __init__(self, outfd, *writer_args, **writer_kw):
        self.writer = csv.writer(self.UnicodeFdWrapper(outfd), *writer_args, **writer_kw)

    def encode_field(self, val):
        encode = getattr(val, "encode", None)
        if encode is not None:
            return encode("utf-8")
        else:
            return val

    def writerow(self, row):
        enc = self.encode_field
        self.writer.writerow([enc(s) for s in row])


class Column(object):


# Comment: Wrap an output file descriptor into something that accepts utf8 byte
strings and forwards unicode
    class UnicodeFdWrapper(object):
        
        def __init__(self, outfd):
            self.outfd = outfd

        def write(self, bytestr):
            self.outfd.write(bytestr.decode("utf-8"))



# Comment: Format an integer to a string, returning '-' if the integer is None.
def intormiss(x):
    
    if x is None:
        return "-"
    else:
        return "%d" % x




# Comment: Perform a DB-All.e query using the given db and query query, and output
the results in CSV format on the given file object
def export(tr, query, fd):
    
    e = Exporter(tr)
    e.output(query, fd)


