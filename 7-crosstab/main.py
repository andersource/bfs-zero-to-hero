##############################################################################
#
#                   BFS zero-to-hero part 7:   Crosstab
#                   -----------------------------------
#
##############################################################################
##############################################################################


import sqlite3


def load_relations():
    # Return value:     Representation of the database relations, in any form you choose
    #
    with open("relations.txt", "r") as f:
        raise NotImplementedError()


def construct_query(col1, col2, aggcol, agg, table_relations):
    # Params:
    #   col1:               String of shape "TableName.ColumnName", indicating first crosstab
    #                       category column
    #
    #   col2:               String of shape "TableName.ColumnName", indicating second crosstab
    #                       category column
    #
    #   aggcol:             String of shape "TableName.ColumnName", indicating crosstab value column
    #
    #   agg:                String denoting desired SQL aggregation function
    #
    #   table_relations:    Object returned by the `load_relations` function
    #
    # Return value:         SQL query for selecting desired crosstab data
    #
    raise NotImplementedError()


##############################################################################
########################    behind-the-scenes code    ########################
##############################################################################
def assert_value(results, k1, k2, v):
    x = [r_v for r_k1, r_k2, r_v in results if r_k1 == k1 and r_k2 == k2]
    if len(x) == 0:
        raise AssertionError(f"No value found for keys {k1}, {k2}")

    assert x[0] == v or x[0] - v < 1e-6


def main():
    con = sqlite3.connect("Chinook_Sqlite.sqlite")
    cur = con.cursor()
    table_relations = load_relations()

    def test1():
        q = construct_query("Playlist.Name", "Genre.Name", "Track.TrackId", "COUNT",
                            table_relations)
        res = cur.execute(q).fetchall()

        assert_value(res, "Grunge", "Alternative", 1)
        assert_value(res, "90’s Music", "Classical", 40)
        assert_value(res, "TV Shows", "Comedy", 34)

    def test2():
        q = construct_query("Genre.Name", "MediaType.Name", "Track.UnitPrice", "AVG",
                            table_relations)
        res = cur.execute(q).fetchall()

        assert_value(res, "Blues", "MPEG audio file", 0.99)
        assert_value(res, "Sci Fi & Fantasy", "Protected MPEG-4 video file", 1.99)

    def test3():
        q = construct_query("Customer.Country", "Genre.Name", "Track.TrackId", "COUNT",
                            table_relations)
        res = cur.execute(q).fetchall()

        assert_value(res, "Argentina", "Jazz", 2)
        assert_value(res, "Hungary", "Rock", 11)
        assert_value(res, "USA", "Heavy Metal", 4)

    test1()
    test2()
    test3()

    print("All tests passed!")


if __name__ == "__main__":
    main()
