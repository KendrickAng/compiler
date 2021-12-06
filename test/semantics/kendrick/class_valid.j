class TestClass {
    Void main(Int a, Bool b, String s, Void v, TestClass t) {
        return;
    }
}

class TestClass1 {
    Dummy j;
    Bool dummy() {
        Bool i;
        return i;
    }
}

class TestClass2 {
    Void main(Int i, Int a, Int b, Int d){
        Int t1;
        Int t2;
        while(true){
            t1 = t2 ;
        }
    }
}

class TestClass3 {
    TestClass3 c;
    Int i;

    Int dummy() {
        Bool i;
        Bool j;
        if (i || j) {
            return 1;
        }
        else {
            while(i) {
                i = !j;
            }
            return 1;
        }
        return this.getCompute().i;
    }

    TestClass3 getCompute() {
        return c;
    }
}
