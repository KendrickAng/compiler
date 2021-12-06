class My_Main_0123 {

   Void main(Int i2, String s2){
      Dummy d;
      d = new Dummy();
      d.aa = new Apple();
      d.bb = new Banana();
      d.cc = new Color();
      d.dd = new Dummy();

      d.aa.seeds = 0;
      d.aa.color = d.cc;
      d.dd = d.init(d.aa, d.bb, d.cc, d.dd, d.aa.seeds, d.aa.isRipe && d.aa.isRipe);
      return;
   }

}

class Apple {
   Int seeds;
   Color color;
   Bool isRipe;
}

class Banana {
   // Empty body
}

class Color {
   String red() {
      return "red";
   }
   Bool canMix(Bool y, Int z) {
      return !false;
   }
}


class Dummy {
   Apple aa;
   Banana bb;
   Color cc;
   Dummy dd;
   Int s;

   Dummy init(Apple a, Banana b, Color c, Dummy d, Int e, Bool f) {
      Dummy gg;
      if (e + d.aa.seeds + a.seeds > e + e - 02 * e + e - e / e) {
         gg = null;
      } else {
         gg = new Dummy();
         gg.aa=a;
         gg.bb=b;
         gg.cc=c;
         gg.dd=this;
         gg.aa.seeds=e+2;
         gg.aa.isRipe=f;
         gg.aa.color=gg.cc;
      }
      return gg;
   }
   Bool dummy() {
      readln ( s );
      println(1+2);
      this.cc = null;
      return this.aa.color.canMix(this.aa.color.canMix(!true, -1) || this.aa.color.canMix(false, 1), s * s);
   }
}