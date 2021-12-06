class TestSExp {
    Void main() {
        TestSExp t;
        t = "hi";
        t = "hi" + "world";
        t = t + "hi";
        t = this + "hi";
        t = this.id + "hi";
        t = new TestSExp() + "hi";
        t = (this.id) + "hi";
        t = (null.id) + "hi";
        t = this.id + this.id.id(1,"c",true) + (1+2-3*4/5) + (true || false && true) + "hi";
        t = "I hate " + "this assignment " + "why can't we use " + " parser generators ? ";
    }
}
