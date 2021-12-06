class Main {
    Void main() {
        return;
    }
}

class Test {
    Void init() {
        println(clone());
    }

    Test clone() {
        return this;
    }
}
