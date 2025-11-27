"""
Cleanup and Reset Script
Removes old models and forces retraining
"""
import os
import shutil

def cleanup_models():
    """Remove old model files"""
    print("=" * 60)
    print("🧹 CLEANUP AND RESET")
    print("=" * 60)
    
    models_dir = 'models'
    
    if os.path.exists(models_dir):
        print(f"\n📁 Found models directory: {models_dir}")
        
        files = os.listdir(models_dir)
        if files:
            print(f"   Found {len(files)} files:")
            for f in files:
                print(f"   - {f}")
            
            response = input("\n❓ Delete these files? (yes/no): ").strip().lower()
            
            if response == 'yes':
                for f in files:
                    file_path = os.path.join(models_dir, f)
                    try:
                        os.remove(file_path)
                        print(f"   ✓ Deleted: {f}")
                    except Exception as e:
                        print(f"   ✗ Could not delete {f}: {e}")
                
                print("\n✓ Cleanup complete!")
                print("📝 Next time you run app.py, models will be retrained.")
            else:
                print("\n⏭️  Cleanup cancelled")
        else:
            print("   No model files found")
    else:
        print(f"\n📁 Models directory does not exist: {models_dir}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    cleanup_models()
