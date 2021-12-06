class Main {

    Void main(){
        Int i;
        i = 2;
    }
}

class Clone {
    Clone other;
    Void methodB() {
        other = methodA();
        return;
    }
    Clone methodA() {
        return this.other;
    }
    
}