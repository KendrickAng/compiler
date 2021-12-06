class Main {

    Void main(){
        Int i;
        i = 2;
    }
}

class Clone {
    
    Clone other;

    Clone methodA() {
        other = new Clone();
        other.other = new Clone();
        (this.methodA().other).methodA().other.methodB();
        return this.other;
    }
/*
    Void methodB() {
        this.methodA();
        other.methodA();
        other.methodB();
        return;
    }
  */  
}