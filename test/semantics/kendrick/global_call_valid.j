class Main {
    Void main(){
        return;
    }
}

class Global {

    Global globe;

    Global getGlobal() {
        Global another;
        another = globe;
        another.globe = globe;
        this.globe.globe = another;
        (this.globe) = another.globe;
        this.globe = getGlobal();
        return globe;
    }

    Void getVoid() {
        this.getGlobal();
        globe.getVoid();
        globe.getGlobal();
        globe.globe.getVoid();
        globe.globe.getGlobal();
        return;
    }

}