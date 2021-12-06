class Main {

    Void main(){
        Local local;
        local.all();
    }
}

class Local {

    Int a() {
        return 1;
    }

    String b() {
        return "hello";
    }

    Bool c() {
        return true;
    }

    Local d() {
        return this;
    }

    Void all() {
        a();
        b();
        c();
        d();
        return;
    }
}