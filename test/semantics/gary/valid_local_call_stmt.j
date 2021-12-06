class Main {

    Void main(){
        Int i;
        i = 2;
    }
}

class Clone {

    Void methodA() {
        methodB();
        return;
    }

    Void methodB() {
        methodA();
        return;
    }
    
}