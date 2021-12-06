class Main {

    Void main(){
        String s;
        Statement statement;
        Int x;

        x = 2;
        statement = new Statement();
        statement.s = new Statement();

        if (x == 0) {
            x = 2;
        } else {
            s = "this is a hard" + "module and why am I spending so much time on this";
        }

        while (x > 0 && false || !!!!true) {
            statement.skip(statement);
        }

        return;
    }
}

class Statement {
    Statement s;

    Statement copy() {
        Statement c;
        skip(c);
        s = new Statement();
        return s;
    }

    Void skip(Statement c) {
        return;
    }
}