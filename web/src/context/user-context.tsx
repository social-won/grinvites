import React, { createContext, useContext, useEffect, useState } from "react";
import { getUser } from "@/lib/api";
import supabase from "@/lib/supabase";
import { AuthChangeEvent, Session } from "@supabase/supabase-js";
import { GrinvitesUser } from "@/lib/utils";

interface UserContextType {
  user: GrinvitesUser | null;
  loading: boolean;
  error: Error | null;
  // refetch: () => Promise<void>;
  setUser: React.Dispatch<React.SetStateAction<GrinvitesUser | null>>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<GrinvitesUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const handleAuthChange = async (_e: AuthChangeEvent, session: Session | null) => {
    console.log(session);
    
    if (!session?.user) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const data = await getUser(session.user.id).catch(console.log);

      if (!data) {
        setUser({
          id: session.user.id,
          email: session.user.email || "",
          prefer_notify: 0
        });
        return;
      }

      setUser(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Unknown error");
      setError(error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const { data: listener } = supabase.auth.onAuthStateChange(handleAuthChange);

    return () => {
      listener?.subscription?.unsubscribe();
    };
  }, []);

  return (
    <UserContext.Provider value={{ user, loading, error, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
