
public abstract class OAHashTable implements IHashTable {
	
	private HashTableElement [] table;
	protected int size;
	
	public OAHashTable(int m) {
		this.table = new HashTableElement[m];
		for(int i = 0; i<m ;i++){
			this.table[i] = null;
		}
		this.size = m;
	}
	
	
	@Override
	public HashTableElement Find(long key) {
		int i=0;
		int m = this.size;
		while(i<m){
			int j = this.Hash(key, i);
			if (this.table[j]==null){
				return null;
			}
			else if(this.table[j].GetKey()==key){
				return this.table[j];
			}
			i++;
			j = this.Hash(key, i);
		}
		return null;
	}
	
	@Override
	public void Insert(HashTableElement hte) throws TableIsFullException,KeyAlreadyExistsException {
		int i = 0;
		int j = this.Hash(hte.GetKey(), i);
		int d = -1;

		while(this.table[j] != null) {
			if (this.table[j].GetKey() == hte.GetKey()){
				throw new KeyAlreadyExistsException(hte);
			}
			if(this.table[j].GetKey() == -1 && d ==-1){
				d = j;
			}
			i++;
			if (i >= this.size){
				throw new TableIsFullException(hte);
			}


			j = this.Hash(hte.GetKey(), i);
		}
		
		if (d == -1){
			this.table[j] = hte;
		}
		else{
			this.table[d] = hte;
		}
	}
	
	@Override
	public void Delete(long key) throws KeyDoesntExistException {
		int i=0;
		int m = this.size;
		HashTableElement deleted = new HashTableElement( -1,0);
		while(i<m){
			int j = this.Hash(key, i);
			if (this.table[j] == null){
				throw new KeyDoesntExistException(key);
			}
			else if(this.table[j].GetKey()==key){
				this.table[j] = deleted;
				return;
			}
			i++;
			j = this.Hash(key, i);
		}
		throw new KeyDoesntExistException(key);
	}
	
	/**
	 * 
	 * @param x - the key to hash
	 * @param i - the index in the probing sequence
	 * @return the index into the hash table to place the key x
	 */
	public abstract int Hash(long x, int i);
}
