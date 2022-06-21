import java.util.concurrent.ThreadLocalRandom;

public class ModHash {

	private int  m;
	private long a, b, p;
	
	public ModHash(long a, long b, int m, long p){
		this.a = a;
		this.b = b;
		this.m = m;
		this.p = p;
	}


	public static ModHash GetFunc(int m, long p){
		long a = 1 + ThreadLocalRandom.current().nextLong(p);
		long b = ThreadLocalRandom.current().nextLong(p);
		return new ModHash(a, b, m, p);
	}
	
	public int Hash(long key) {
		return (int)((((long)(this.a) * (long)key + (long)this.b) % this.p) % this.m);
	}
}
