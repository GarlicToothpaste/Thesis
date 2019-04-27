import sys;

def test(x , y ,z ):
    print("First argument is:", x);
    print("Second argument is:", y);
    print("Third argument is:" ,z);

test( sys.argv[1], sys.argv[2], sys.argv[3]);
