class My_Main_0123 {

   Void main(Int i2, String s2){
      Dummy d;
      d = new Dummy();
      d.aa = 1;
      d.bb = true;
      d.cc = " ";
      d.dd = new Dummy();

      d.dd.seeds = 0;
      d.dd.cc = d.cc;
      d.dd = d.init(d.aa, d.bb, d.cc, d.dd, -4567, d.dummy() && !d.dummy());
      return;
   }

}

class Dummy {
   Int aa;
   Bool bb;
   String cc;
   Dummy dd;
   Int seeds;

   Dummy init(Int a, Bool b, String c, Dummy d, Int e, Bool f) {
      Dummy gg;
      if (e + d.aa + a > e + e - 02 * e + e - e / e) {
         return this.dd;
         gg = null;
      } else {
         gg = new Dummy();
         gg.aa=a;
         gg.bb=b;
         gg.cc=c;
         gg.dd=this;
      }
      return gg;
   }
   Bool dummy() {
      Bool s;
      readln ( s );
      println(1+2);
      this.cc = null;
      return this.dummy();
   }
}